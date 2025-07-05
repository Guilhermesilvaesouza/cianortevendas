import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.product import Product
from src.models.order import Order, OrderItem
from src.models.payment import Payment
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.product import product_bp
from src.routes.order import order_bp
from src.routes.payment import payment_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitar CORS para permitir requisições do frontend
CORS(app)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(order_bp, url_prefix='/api')
app.register_blueprint(payment_bp, url_prefix='/api')

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    
    # Criar alguns produtos de exemplo se não existirem
    if Product.query.count() == 0:
        sample_products = [
            Product(
                name="Smartphone Samsung Galaxy A54",
                description="Smartphone com tela de 6.4 polegadas, 128GB de armazenamento e câmera tripla de 50MP.",
                price=1299.99,
                category="Eletrônicos",
                stock_quantity=10,
                image_url="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"
            ),
            Product(
                name="Notebook Dell Inspiron 15",
                description="Notebook com processador Intel Core i5, 8GB RAM, SSD 256GB e tela de 15.6 polegadas.",
                price=2499.99,
                category="Eletrônicos",
                stock_quantity=5,
                image_url="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400"
            ),
            Product(
                name="Tênis Nike Air Max",
                description="Tênis esportivo confortável para corrida e caminhada, disponível em várias cores.",
                price=299.99,
                category="Calçados",
                stock_quantity=20,
                image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"
            ),
            Product(
                name="Camiseta Polo Lacoste",
                description="Camiseta polo clássica de algodão, disponível em várias cores e tamanhos.",
                price=189.99,
                category="Roupas",
                stock_quantity=15,
                image_url="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400"
            ),
            Product(
                name="Fone de Ouvido Sony WH-1000XM4",
                description="Fone de ouvido com cancelamento de ruído ativo e qualidade de som premium.",
                price=899.99,
                category="Eletrônicos",
                stock_quantity=8,
                image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"
            )
        ]
        
        for product in sample_products:
            db.session.add(product)
        
        db.session.commit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

