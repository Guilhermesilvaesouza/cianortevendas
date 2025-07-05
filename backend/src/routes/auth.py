from flask import Blueprint, jsonify, request
from src.models.user import User, db
import jwt
import datetime
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# Chave secreta para JWT (em produção, use uma variável de ambiente)
SECRET_KEY = 'asdf#FGSgvasgf$5$WGT'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token é necessário!'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token inválido!'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    
    # Verificar se o usuário já existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email já cadastrado!'}), 400
    
    if User.query.filter_by(cpf=data['cpf']).first():
        return jsonify({'message': 'CPF já cadastrado!'}), 400
    
    # Criar novo usuário
    user = User(
        name=data['name'],
        email=data['email'],
        cpf=data['cpf'],
        phone=data.get('phone'),
        address=data.get('address')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'token': token,
            'user': user.to_dict()
        })
    
    return jsonify({'message': 'Email ou senha inválidos!'}), 401

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify(current_user.to_dict())

@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.json
    
    current_user.name = data.get('name', current_user.name)
    current_user.phone = data.get('phone', current_user.phone)
    current_user.address = data.get('address', current_user.address)
    
    db.session.commit()
    
    return jsonify(current_user.to_dict())

