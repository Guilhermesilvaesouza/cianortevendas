from flask import Blueprint, jsonify, request
from src.models.order import Order, OrderItem
from src.models.product import Product
from src.models.user import db
from src.routes.auth import token_required

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['POST'])
@token_required
def create_order(current_user):
    data = request.json
    
    # Calcular o total do pedido
    total = 0
    order_items_data = data.get('items', [])
    
    # Verificar se todos os produtos existem e calcular total
    for item_data in order_items_data:
        product = Product.query.get(item_data['product_id'])
        if not product:
            return jsonify({'message': f'Produto {item_data["product_id"]} não encontrado!'}), 400
        
        if product.stock_quantity < item_data['quantity']:
            return jsonify({'message': f'Estoque insuficiente para o produto {product.name}!'}), 400
        
        total += product.price * item_data['quantity']
    
    # Criar o pedido
    order = Order(
        user_id=current_user.id,
        total=total
    )
    
    db.session.add(order)
    db.session.flush()  # Para obter o ID do pedido
    
    # Criar os itens do pedido
    for item_data in order_items_data:
        product = Product.query.get(item_data['product_id'])
        
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item_data['quantity'],
            unit_price=product.price
        )
        
        # Atualizar estoque
        product.stock_quantity -= item_data['quantity']
        
        db.session.add(order_item)
    
    db.session.commit()
    
    return jsonify(order.to_dict()), 201

@order_bp.route('/orders', methods=['GET'])
@token_required
def get_user_orders(current_user):
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).all()
    
    orders_data = []
    for order in orders:
        order_dict = order.to_dict()
        order_dict['items'] = [item.to_dict() for item in order.items]
        orders_data.append(order_dict)
    
    return jsonify(orders_data)

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
@token_required
def get_order(current_user, order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    order_dict = order.to_dict()
    order_dict['items'] = []
    
    for item in order.items:
        item_dict = item.to_dict()
        item_dict['product'] = item.product.to_dict()
        order_dict['items'].append(item_dict)
    
    return jsonify(order_dict)

@order_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    # Esta rota pode ser usada por webhooks ou administradores
    data = request.json
    order = Order.query.get_or_404(order_id)
    
    order.status = data.get('status', order.status)
    db.session.commit()
    
    return jsonify(order.to_dict())

