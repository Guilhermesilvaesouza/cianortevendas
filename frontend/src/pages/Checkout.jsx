import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { CreditCard, QrCode, ArrowLeft } from 'lucide-react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { orderService } from '../services/api';
import axios from 'axios';

const Checkout = () => {
  const { items, getTotal, clearCart } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();
  
  const [step, setStep] = useState(1); // 1: Resumo, 2: Pagamento, 3: Confirmação
  const [paymentMethod, setPaymentMethod] = useState('');
  const [loading, setLoading] = useState(false);
  const [order, setOrder] = useState(null);
  const [paymentData, setPaymentData] = useState(null);

  useEffect(() => {
    if (items.length === 0) {
      navigate('/cart');
    }
  }, [items, navigate]);

  const createOrder = async () => {
    try {
      setLoading(true);
      
      const orderData = {
        items: items.map(item => ({
          product_id: item.id,
          quantity: item.quantity
        }))
      };
      
      const response = await orderService.createOrder(orderData);
      setOrder(response.data);
      setStep(2);
    } catch (error) {
      console.error('Erro ao criar pedido:', error);
      alert('Erro ao criar pedido. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const processPayment = async () => {
    if (!order || !paymentMethod) return;
    
    try {
      setLoading(true);
      
      const paymentData = {
        order_id: order.id,
        payment_method: paymentMethod
      };
      
      const response = await axios.post('/api/create-payment', paymentData, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      setPaymentData(response.data);
      setStep(3);
      
      // Se for PIX, mostrar QR Code
      if (paymentMethod === 'pix') {
        // QR Code será exibido na próxima etapa
      }
      
      // Limpar carrinho após pagamento criado
      clearCart();
      
    } catch (error) {
      console.error('Erro ao processar pagamento:', error);
      alert('Erro ao processar pagamento. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const checkPaymentStatus = async () => {
    if (!paymentData?.payment_id) return;
    
    try {
      const response = await axios.get(`/api/payment-status/${paymentData.payment_id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      const status = response.data.status;
      
      if (status === 'approved') {
        alert('Pagamento aprovado! Seu pedido está sendo processado.');
        navigate('/profile');
      } else if (status === 'rejected') {
        alert('Pagamento recusado. Tente novamente.');
        setStep(2);
      }
    } catch (error) {
      console.error('Erro ao verificar status do pagamento:', error);
    }
  };

  if (step === 1) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto">
            <div className="flex items-center mb-8">
              <Button
                variant="outline"
                onClick={() => navigate('/cart')}
                className="mr-4"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Voltar ao Carrinho
              </Button>
              <h1 className="text-3xl font-bold text-gray-900">Finalizar Compra</h1>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <h2 className="text-xl font-semibold mb-4">Resumo do Pedido</h2>
              
              <div className="space-y-4 mb-6">
                {items.map((item) => (
                  <div key={item.id} className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <img
                        src={item.image_url || 'https://via.placeholder.com/60'}
                        alt={item.name}
                        className="w-12 h-12 object-cover rounded"
                      />
                      <div>
                        <p className="font-medium">{item.name}</p>
                        <p className="text-sm text-gray-600">
                          Qtd: {item.quantity} x R$ {item.price.toFixed(2)}
                        </p>
                      </div>
                    </div>
                    <p className="font-semibold">
                      R$ {(item.price * item.quantity).toFixed(2)}
                    </p>
                  </div>
                ))}
              </div>
              
              <div className="border-t pt-4">
                <div className="flex justify-between text-xl font-bold">
                  <span>Total:</span>
                  <span className="text-green-600">R$ {getTotal().toFixed(2)}</span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">Dados de Entrega</h2>
              <div className="space-y-2">
                <p><strong>Nome:</strong> {user?.name}</p>
                <p><strong>Email:</strong> {user?.email}</p>
                <p><strong>CPF:</strong> {user?.cpf}</p>
                {user?.address && <p><strong>Endereço:</strong> {user.address}</p>}
                {user?.phone && <p><strong>Telefone:</strong> {user.phone}</p>}
              </div>
              
              <Button
                onClick={createOrder}
                disabled={loading}
                className="w-full mt-6"
              >
                {loading ? 'Criando Pedido...' : 'Continuar para Pagamento'}
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (step === 2) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Escolha a Forma de Pagamento</h1>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="space-y-4 mb-6">
                <div
                  className={`border-2 rounded-lg p-4 cursor-pointer transition-colors ${
                    paymentMethod === 'pix' ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
                  }`}
                  onClick={() => setPaymentMethod('pix')}
                >
                  <div className="flex items-center space-x-3">
                    <QrCode className="h-6 w-6 text-blue-600" />
                    <div>
                      <h3 className="font-semibold">PIX</h3>
                      <p className="text-sm text-gray-600">Pagamento instantâneo</p>
                    </div>
                  </div>
                </div>

                <div
                  className={`border-2 rounded-lg p-4 cursor-pointer transition-colors ${
                    paymentMethod === 'credit_card' ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
                  }`}
                  onClick={() => setPaymentMethod('credit_card')}
                >
                  <div className="flex items-center space-x-3">
                    <CreditCard className="h-6 w-6 text-blue-600" />
                    <div>
                      <h3 className="font-semibold">Cartão de Crédito</h3>
                      <p className="text-sm text-gray-600">Parcelamento disponível</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="border-t pt-4 mb-6">
                <div className="flex justify-between text-xl font-bold">
                  <span>Total a Pagar:</span>
                  <span className="text-green-600">R$ {getTotal().toFixed(2)}</span>
                </div>
              </div>

              <div className="flex space-x-4">
                <Button
                  variant="outline"
                  onClick={() => setStep(1)}
                  className="flex-1"
                >
                  Voltar
                </Button>
                
                <Button
                  onClick={processPayment}
                  disabled={!paymentMethod || loading}
                  className="flex-1"
                >
                  {loading ? 'Processando...' : 'Confirmar Pagamento'}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (step === 3) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Pagamento</h1>

            <div className="bg-white rounded-lg shadow-md p-6">
              {paymentMethod === 'pix' && paymentData?.qr_code && (
                <div className="text-center">
                  <h2 className="text-xl font-semibold mb-4">Pague com PIX</h2>
                  <p className="text-gray-600 mb-6">
                    Escaneie o QR Code abaixo ou copie o código PIX
                  </p>
                  
                  {paymentData.qr_code_base64 && (
                    <div className="mb-6">
                      <img
                        src={`data:image/png;base64,${paymentData.qr_code_base64}`}
                        alt="QR Code PIX"
                        className="mx-auto"
                      />
                    </div>
                  )}
                  
                  <div className="bg-gray-100 p-4 rounded-lg mb-6">
                    <p className="text-sm text-gray-600 mb-2">Código PIX:</p>
                    <p className="font-mono text-sm break-all">{paymentData.qr_code}</p>
                    <Button
                      variant="outline"
                      size="sm"
                      className="mt-2"
                      onClick={() => navigator.clipboard.writeText(paymentData.qr_code)}
                    >
                      Copiar Código
                    </Button>
                  </div>
                  
                  <Button onClick={checkPaymentStatus} className="w-full">
                    Verificar Pagamento
                  </Button>
                </div>
              )}

              {paymentMethod === 'credit_card' && (
                <div className="text-center">
                  <h2 className="text-xl font-semibold mb-4">Pagamento com Cartão</h2>
                  <p className="text-gray-600 mb-6">
                    Seu pagamento está sendo processado...
                  </p>
                  
                  <Button onClick={checkPaymentStatus} className="w-full">
                    Verificar Status do Pagamento
                  </Button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default Checkout;

