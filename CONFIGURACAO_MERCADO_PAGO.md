# Configuração do Mercado Pago - Guia Passo a Passo

## 📋 Pré-requisitos

- Conta no Mercado Pago (pessoa física aceita)
- CPF válido
- Conta bancária para recebimento

## 🔧 Passo 1: Criar Conta no Mercado Pago

1. Acesse: https://www.mercadopago.com.br
2. Clique em "Criar conta"
3. Escolha "Quero vender"
4. Preencha seus dados pessoais
5. Confirme seu email e telefone

## 🔑 Passo 2: Acessar Painel de Desenvolvedores

1. Faça login na sua conta Mercado Pago
2. Acesse: https://www.mercadopago.com.br/developers
3. Clique em "Suas integrações"
4. Clique em "Criar aplicação"

## 📱 Passo 3: Criar Aplicação

1. **Nome da aplicação**: "Cianorte Vendas"
2. **Modelo de negócio**: "Marketplace"
3. **Produtos**: Selecione "Checkout Pro" e "Checkout API"
4. **Clique em "Criar aplicação"**

## 🔐 Passo 4: Obter Credenciais

### Ambiente de Testes (para desenvolvimento)
1. Na sua aplicação, vá para "Credenciais"
2. Copie o **Access Token de teste**
3. Use este token durante o desenvolvimento

### Ambiente de Produção (para site real)
1. Complete a verificação da sua conta
2. Adicione dados bancários para recebimento
3. Na seção "Credenciais", copie o **Access Token de produção**

## ⚙️ Passo 5: Configurar no Site

### Backend (Flask)
Edite o arquivo: `backend/src/routes/payment.py`

```python
# Linha 8 - Substitua pelo seu Access Token
mp = mercadopago.SDK("APP_USR-SEU_ACCESS_TOKEN_AQUI")
```

### Exemplo de Access Token:
```
APP_USR-1234567890123456-123456-abcdef1234567890abcdef1234567890-123456789
```

## 🧪 Passo 6: Testar Integração

### Cartões de Teste (Ambiente de Testes)
- **Visa**: 4509 9535 6623 3704
- **Mastercard**: 5031 7557 3453 0604
- **CVV**: 123
- **Vencimento**: 11/25

### PIX de Teste
- Use CPF: 12345678909
- O pagamento será aprovado automaticamente

## 💰 Passo 7: Configurar Recebimento

1. **Conta bancária**: Adicione sua conta no painel Mercado Pago
2. **Prazo de recebimento**: 
   - PIX: Instantâneo
   - Cartão: 14 dias (padrão) ou 30 dias
3. **Taxas**:
   - PIX: 0,99%
   - Cartão de crédito: 4,99% + R$ 0,39
   - Cartão de débito: 2,99% + R$ 0,39

## 🔒 Passo 8: Ativar Produção

1. **Verificação de conta**: Complete todos os dados solicitados
2. **Homologação**: Teste todos os fluxos de pagamento
3. **Ativação**: Solicite ativação da conta para produção
4. **Substitua** o Access Token de teste pelo de produção

## 📊 Passo 9: Monitoramento

### Painel Mercado Pago
- Acompanhe vendas em tempo real
- Visualize relatórios financeiros
- Gerencie estornos e disputas

### Webhooks (Opcional)
Configure notificações automáticas para:
- Pagamentos aprovados
- Pagamentos rejeitados
- Estornos

## ⚠️ Importantes

### Segurança
- **NUNCA** compartilhe seu Access Token
- Use HTTPS em produção (obrigatório)
- Valide dados no backend

### Compliance
- Mantenha dados de clientes seguros
- Siga a LGPD para dados pessoais
- Implemente logs de auditoria

### Suporte
- **Documentação**: https://www.mercadopago.com.br/developers/pt/docs
- **Suporte técnico**: https://www.mercadopago.com.br/developers/pt/support
- **Status da API**: https://status.mercadopago.com/

## 🚀 Próximos Passos

1. ✅ Criar conta Mercado Pago
2. ✅ Obter Access Token de teste
3. ✅ Configurar no código
4. ✅ Testar pagamentos
5. ⏳ Verificar conta para produção
6. ⏳ Obter Access Token de produção
7. ⏳ Ativar site em produção

---

**Dúvidas?** Consulte a documentação oficial do Mercado Pago ou entre em contato com o suporte técnico.

