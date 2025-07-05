from src.models.user import db
from datetime import datetime

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # PIX, Cartão de Crédito
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default='Pendente')  # Pendente, Aprovado, Recusado, Reembolsado
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_id = db.Column(db.String(100), nullable=True)  # ID da transação no Mercado Pago

    # Relacionamento com Order
    order = db.relationship('Order', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f'<Payment {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'payment_method': self.payment_method,
            'amount': self.amount,
            'payment_status': self.payment_status,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'transaction_id': self.transaction_id
        }

