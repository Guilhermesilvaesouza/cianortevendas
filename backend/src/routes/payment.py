from flask import Blueprint, jsonify, request
import mercadopago
from src.models.payment import Payment
from src.models.order import Order
from src.models.user import db
from src.routes.auth import token_required
import os

payment_bp = Blueprint('payment', __name__)

# Configuração do Mercado Pago (em produção, use variáveis de ambiente)
# Para testes, você pode usar o access token de teste
MP_ACCESS_TOKEN = os.getenv('MP_ACCESS_TOKEN', 'TEST-YOUR_ACCESS_TOKEN_HERE')
sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

@payment_bp.route('/create-payment', methods=['POST'])
@token_required
def create_payment(current_user):
    try:
        data = request.json
        order_id = data.get('order_id')
        payment_method = data.get('payment_method')  # 'pix' ou 'credit_card'
        
        # Buscar o pedido
        order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()
        if not order:
            return jsonify({'error': 'Pedido não encontrado'}), 404
        
        # Dados do pagamento para o Mercado Pago
        payment_data = {
            "transaction_amount": float(order.total),
            "description": f"Pedido #{order.id} - Cianorte Vendas",
            "payment_method_id": payment_method,
            "payer": {
                "email": current_user.email,
                "first_name": current_user.name.split()[0] if current_user.name else "Cliente",
                "last_name": " ".join(current_user.name.split()[1:]) if len(current_user.name.split()) > 1 else "",
                "identification": {
                    "type": "CPF",
                    "number": current_user.cpf.replace(".", "").replace("-", "") if current_user.cpf else ""
                }
            }
        }
        
        # Para PIX
        if payment_method == 'pix':
            payment_data["payment_method_id"] = "pix"
            
        # Para cartão de crédito, você precisará dos dados do cartão
        elif payment_method == 'credit_card':
            card_data = data.get('card_data', {})
            payment_data.update({
                "token": card_data.get('token'),  # Token do cartão gerado pelo frontend
                "installments": card_data.get('installments', 1),
                "payment_method_id": card_data.get('payment_method_id'),
                "issuer_id": card_data.get('issuer_id')
            })
        
        # Criar pagamento no Mercado Pago
        payment_response = sdk.payment().create(payment_data)
        payment_result = payment_response["response"]
        
        if payment_response["status"] == 201:
            # Salvar pagamento no banco de dados
            payment = Payment(
                order_id=order.id,
                payment_method=payment_method,
                amount=order.total,
                payment_status='Pendente',
                transaction_id=str(payment_result.get('id'))
            )
            
            db.session.add(payment)
            
            # Atualizar status do pedido
            order.status = 'Processando'
            db.session.commit()
            
            # Retornar dados do pagamento
            response_data = {
                'payment_id': payment_result.get('id'),
                'status': payment_result.get('status'),
                'status_detail': payment_result.get('status_detail'),
                'payment_method': payment_method
            }
            
            # Para PIX, incluir dados do QR Code
            if payment_method == 'pix':
                response_data.update({
                    'qr_code': payment_result.get('point_of_interaction', {}).get('transaction_data', {}).get('qr_code'),
                    'qr_code_base64': payment_result.get('point_of_interaction', {}).get('transaction_data', {}).get('qr_code_base64'),
                    'ticket_url': payment_result.get('point_of_interaction', {}).get('transaction_data', {}).get('ticket_url')
                })
            
            return jsonify(response_data), 201
        else:
            return jsonify({'error': 'Erro ao criar pagamento', 'details': payment_result}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/payment-status/<payment_id>', methods=['GET'])
@token_required
def get_payment_status(current_user, payment_id):
    try:
        # Buscar status no Mercado Pago
        payment_response = sdk.payment().get(payment_id)
        
        if payment_response["status"] == 200:
            payment_data = payment_response["response"]
            
            # Atualizar status no banco de dados
            payment = Payment.query.filter_by(transaction_id=payment_id).first()
            if payment:
                mp_status = payment_data.get('status')
                
                if mp_status == 'approved':
                    payment.payment_status = 'Aprovado'
                    payment.order.status = 'Processando'
                elif mp_status == 'rejected':
                    payment.payment_status = 'Recusado'
                    payment.order.status = 'Cancelado'
                elif mp_status == 'pending':
                    payment.payment_status = 'Pendente'
                
                db.session.commit()
            
            return jsonify({
                'status': payment_data.get('status'),
                'status_detail': payment_data.get('status_detail'),
                'payment_method': payment_data.get('payment_method_id')
            })
        else:
            return jsonify({'error': 'Pagamento não encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/webhook', methods=['POST'])
def webhook():
    """Webhook para receber notificações do Mercado Pago"""
    try:
        data = request.json
        
        if data.get('type') == 'payment':
            payment_id = data.get('data', {}).get('id')
            
            if payment_id:
                # Buscar dados do pagamento
                payment_response = sdk.payment().get(payment_id)
                
                if payment_response["status"] == 200:
                    payment_data = payment_response["response"]
                    
                    # Atualizar status no banco de dados
                    payment = Payment.query.filter_by(transaction_id=str(payment_id)).first()
                    if payment:
                        mp_status = payment_data.get('status')
                        
                        if mp_status == 'approved':
                            payment.payment_status = 'Aprovado'
                            payment.order.status = 'Processando'
                        elif mp_status == 'rejected':
                            payment.payment_status = 'Recusado'
                            payment.order.status = 'Cancelado'
                        elif mp_status == 'pending':
                            payment.payment_status = 'Pendente'
                        
                        db.session.commit()
        
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        print(f"Erro no webhook: {e}")
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/payment-methods', methods=['GET'])
def get_payment_methods():
    """Retorna os métodos de pagamento disponíveis"""
    try:
        payment_methods_response = sdk.payment_methods().list_all()
        
        if payment_methods_response["status"] == 200:
            methods = payment_methods_response["response"]
            
            # Filtrar apenas PIX e cartões de crédito
            filtered_methods = []
            for method in methods:
                if method.get('id') == 'pix' or method.get('payment_type_id') == 'credit_card':
                    filtered_methods.append({
                        'id': method.get('id'),
                        'name': method.get('name'),
                        'payment_type_id': method.get('payment_type_id'),
                        'thumbnail': method.get('thumbnail')
                    })
            
            return jsonify(filtered_methods)
        else:
            return jsonify({'error': 'Erro ao buscar métodos de pagamento'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

