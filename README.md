# API de Pagamentos com Azure (Python FastAPI)

## 📌 Descrição
Projeto para simulação de pagamentos, focado em segurança, controle de acesso, gerenciamento de APIs e integração com recursos do Azure.

## 🎯 Objetivos
- ✅ Criar uma API para simulação de pagamentos
- ✅ Implementar controle de acesso e autenticação JWT
- ✅ Utilizar conceitos de API Management
- ✅ Aplicar boas práticas de segurança
- ✅ Estruturar um projeto pronto para portfólio

## 🛠️ Tecnologias Utilizadas
- **FastAPI** - Framework moderno e rápido
- **Uvicorn** - Servidor ASGI
- **Python-Jose** - JWT para autenticação
- **Passlib** - Hash seguro de senhas com bcrypt
- **SlowAPI** - Rate limiting robusto
- **Pytest** - Testes automatizados
- **Azure API Management** - Gateway de API
- **REST API** - JSON, HTTP (GET, POST, PUT, DELETE)

## 📁 Estrutura do Projeto

```
dio_pagamento_python/
├── app/
│   ├── main.py                 # Inicialização e configuração
│   ├── controllers/            # Lógica dos endpoints
│   │   ├── auth_controller.py
│   │   └── pagamento_controller.py
│   ├── routes/                 # Definição das rotas
│   │   ├── auth.py
│   │   └── pagamento.py
│   ├── services/               # Regras de negócio
│   │   └── pagamento_service.py
│   ├── models/                 # Modelos Pydantic
│   │   └── pagamento.py
│   └── middlewares/            # Autenticação, rate limit e logs
│       ├── auth.py
│       └── rate_limit.py
├── tests/                      # Testes automatizados
│   └── test_api.py
├── logs/                       # Arquivos de log
├── .env.example               # Configurações de exemplo
├── requirements.txt           # Dependências Python
└── README.md
```

## 🔒 Recursos de Segurança

✅ **Autenticação JWT** - Tokens HS256 para acesso seguro  
✅ **Criptografia de Senhas** - Bcrypt para proteção  
✅ **Rate Limiting** - Limite de requisições por minuto  
✅ **Validação de Dados** - Pydantic com tipos e constraints  
✅ **Middleware de Autenticação** - Proteção de endpoints  
✅ **CORS Configurado** - Controle de origem  
✅ **Logging Estruturado** - Rastreamento de operações  
✅ **Variáveis de Ambiente** - Proteção de segredos  

## 📊 Features Implementadas

### Endpoints Disponíveis

#### Health Check
```http
GET /
```
Retorna status da API e timestamp

#### Autenticação
```http
POST /auth/login
```
Credenciais padrão para teste:
- **Username**: `usuario_demo`
- **Password**: `senha123`

#### Pagamentos
```http
GET /pagamentos/               # Listar (30 req/min)
POST /pagamentos/              # Criar (10 req/min, autenticado)
PUT /pagamentos/{id}           # Atualizar (10 req/min, autenticado)
DELETE /pagamentos/{id}        # Deletar (10 req/min, autenticado)
```

### Tipos de Pagamento
```python
{
    "id": 1,
    "valor": 150.50,
    "descricao": "Descrição do pagamento",
    "status": "pendente|processando|concluido|falha|cancelado"
}
```

## 🚀 Como Executar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env e definir JWT_SECRET
JWT_SECRET=sua_chave_secreta_super_segura
```

### 3. Executar o Servidor
```bash
# Modo desenvolvimento (com reload automático)
uvicorn app.main:app --reload

# Modo produção
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

A API estará disponível em:
- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc

## 🧪 Executar Testes

### Todos os testes
```bash
pytest
```

### Com cobertura de código
```bash
pytest --cov=app tests/
```

### Modo verbose
```bash
pytest -v
```

## 📝 Exemplos de Uso

### 1. Fazer Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario_demo", "password": "senha123"}'
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Listar Pagamentos
```bash
curl -X GET "http://localhost:8000/pagamentos/"
```

### 3. Criar Pagamento (requer autenticação)
```bash
curl -X POST "http://localhost:8000/pagamentos/" \
  -H "Authorization: Bearer {seu_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "valor": 150.50,
    "descricao": "Pagamento de serviços",
    "status": "pendente"
  }'
```

### 4. Atualizar Pagamento
```bash
curl -X PUT "http://localhost:8000/pagamentos/1" \
  -H "Authorization: Bearer {seu_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "valor": 200.00,
    "descricao": "Pagamento atualizado"
  }'
```

### 5. Deletar Pagamento
```bash
curl -X DELETE "http://localhost:8000/pagamentos/1" \
  -H "Authorization: Bearer {seu_token}"
```

## 📊 Logs

Os logs são salvos em `logs/api.log` e também exibidos no console. Informações registradas:

- 🟢 Inicialização e shutdown da API
- 🔵 Requisições de autenticação
- 🟡 Operações de CRUD
- 🔴 Erros e exceções
- ⚠️ Excesso de rate limit

## 🔮 Evolução Futura

### Curto Prazo (Próximos Sprint)
- [ ] Integração com banco de dados (PostgreSQL/MongoDB)
- [ ] Refresh tokens para JWT
- [ ] Email notifications para pagamentos
- [ ] Dashboard de relatórios

### Médio Prazo
- [ ] Integração com Azure Cosmos DB
- [ ] Azure Key Vault para secrets
- [ ] Application Insights para monitoramento
- [ ] Docker containerização
- [ ] CI/CD com GitHub Actions

### Longo Prazo
- [ ] Integração com gateways reais (Stripe, PayPal)
- [ ] Machine Learning para detecção de fraudes
- [ ] Sub-domínios e multi-tenancy
- [ ] GraphQL API
- [ ] Deploy em Azure App Service

## 📖 Boas Práticas Implementadas

✅ **Separação em Camadas** - Controllers, Services, Models  
✅ **Type Hints** - Tipagem completa de Python  
✅ **Validação de Dados** - Pydantic models  
✅ **Tratamento de Erros** - Exceções estruturadas  
✅ **Logging** - Rastreamento de operações  
✅ **Testes Automatizados** - Cobertura de endpoints  
✅ **Documentação Automática** - Swagger/OpenAPI  
✅ **Segurança** - JWT, bcrypt, rate limit  
✅ **Variáveis de Ambiente** - Configuração externa  

## 🤝 Contribuindo

Este é um projeto educacional. Sinta-se livre para fazer fork e adicionar melhorias!

## 📚 Recursos Adicionais

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [JWT.io](https://jwt.io/)
- [SlowAPI Rate Limiting](https://github.com/laurents/slowapi)
- [Azure API Management](https://docs.microsoft.com/en-us/azure/api-management/)
- [RESTful API Best Practices](https://restfulapi.net/)

## 📄 Licença

Este projeto é fornecido como material de aprendizado.

---

**Desenvolvido como parte do bootcamp da DIO - Digital Innovation One**
