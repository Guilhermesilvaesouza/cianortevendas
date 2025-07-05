# Cianorte Vendas - Site de E-commerce

Um site de vendas completo desenvolvido com React (frontend) e Flask (backend), integrado com a API do Mercado Pago para processamento de pagamentos via PIX e cartão de crédito.

## 🚀 Funcionalidades

### ✅ Implementadas
- **Catálogo de Produtos**: Exibição de produtos com imagens, preços e descrições
- **Filtros por Categoria**: Eletrônicos, Calçados, Roupas
- **Sistema de Usuários**: Cadastro e login de usuários
- **Carrinho de Compras**: Adicionar/remover produtos do carrinho
- **Checkout**: Processo de finalização de compra
- **Integração Mercado Pago**: Preparado para pagamentos via PIX e cartão
- **Design Responsivo**: Compatível com desktop e mobile
- **API RESTful**: Backend completo com Flask

### 🔧 Configurações Necessárias
- **Mercado Pago**: Configurar Access Token para produção
- **Banco de Dados**: SQLite (desenvolvimento) ou PostgreSQL (produção)

## 📁 Estrutura do Projeto

```
cianorte_vendas/
├── backend/                 # API Flask
│   ├── src/
│   │   ├── models/         # Modelos de dados
│   │   ├── routes/         # Rotas da API
│   │   └── main.py         # Arquivo principal
│   ├── venv/               # Ambiente virtual Python
│   └── requirements.txt    # Dependências Python
├── frontend/               # Aplicação React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── pages/          # Páginas da aplicação
│   │   ├── services/       # Serviços de API
│   │   └── context/        # Contextos React
│   ├── package.json        # Dependências Node.js
│   └── index.html          # Página principal
└── README.md               # Esta documentação
```

## 🛠️ Como Executar

### Backend (Flask)
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```
O backend estará disponível em: http://localhost:5000

### Frontend (React)
```bash
cd frontend
pnpm install
pnpm run dev
```
O frontend estará disponível em: http://localhost:5173

## 🔑 Configuração do Mercado Pago

### 1. Criar Conta no Mercado Pago
- Acesse: https://www.mercadopago.com.br
- Crie uma conta pessoal (pessoa física é aceita)
- Acesse o painel de desenvolvedores

### 2. Obter Credenciais
- Acesse: https://www.mercadopago.com.br/developers/panel/app
- Crie uma aplicação
- Copie o **Access Token** de produção

### 3. Configurar no Backend
Edite o arquivo `backend/src/routes/payment.py` e substitua:
```python
# Linha 8
mp = mercadopago.SDK("SEU_ACCESS_TOKEN_AQUI")
```

## 💳 Tipos de Pagamento Suportados

### PIX
- Pagamento instantâneo
- QR Code gerado automaticamente
- Confirmação em tempo real

### Cartão de Crédito
- Todas as bandeiras aceitas pelo Mercado Pago
- Parcelamento disponível
- Processamento seguro

## 👥 Sistema de Usuários

### Cadastro
- Nome completo
- Email (único)
- CPF
- Telefone (opcional)
- Endereço (opcional)
- Senha

### Login
- Email e senha
- Token JWT para autenticação
- Sessão persistente

## 🛒 Fluxo de Compra

1. **Navegação**: Cliente navega pelos produtos
2. **Carrinho**: Adiciona produtos ao carrinho
3. **Login**: Faz login ou cria conta
4. **Checkout**: Revisa pedido e escolhe pagamento
5. **Pagamento**: Processa via Mercado Pago
6. **Confirmação**: Recebe confirmação do pedido

## 🔧 Personalização

### Adicionar Produtos
Edite o arquivo `backend/src/main.py` na função `create_sample_data()` para adicionar novos produtos.

### Modificar Design
- Cores: Edite `frontend/src/App.css`
- Layout: Modifique componentes em `frontend/src/components/`
- Páginas: Altere arquivos em `frontend/src/pages/`

### Configurar Categorias
Adicione novas categorias no backend e frontend conforme necessário.

## 🚀 Deploy em Produção

### Backend
- Use um servidor WSGI como Gunicorn
- Configure banco PostgreSQL
- Configure variáveis de ambiente para credenciais

### Frontend
- Execute `pnpm run build`
- Sirva os arquivos estáticos via nginx ou similar
- Configure HTTPS obrigatório para pagamentos

## 📞 Suporte

Para dúvidas sobre:
- **Mercado Pago**: https://www.mercadopago.com.br/developers/pt/support
- **React**: https://react.dev/
- **Flask**: https://flask.palletsprojects.com/

## 📝 Próximos Passos

1. **Configurar Mercado Pago**: Adicionar Access Token real
2. **Testar Pagamentos**: Usar ambiente de testes do Mercado Pago
3. **Deploy**: Colocar em produção
4. **Monitoramento**: Implementar logs e métricas
5. **SEO**: Otimizar para motores de busca

---

**Desenvolvido para Cianorte Vendas** 🛍️

