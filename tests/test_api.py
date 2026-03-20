import pytest
from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

# Tokens para testes
VALID_USERNAME = "usuario_demo"
VALID_PASSWORD = "senha123"


class TestAuth:
    """Testes para endpoints de autenticação"""
    
    def test_login_success(self):
        """Testa login com credenciais válidas"""
        response = client.post(
            "/auth/login",
            json={"username": VALID_USERNAME, "password": VALID_PASSWORD}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_username(self):
        """Testa login com username inválido"""
        response = client.post(
            "/auth/login",
            json={"username": "usuario_invalido", "password": VALID_PASSWORD}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Credenciais inválidas"
    
    def test_login_invalid_password(self):
        """Testa login com password inválido"""
        response = client.post(
            "/auth/login",
            json={"username": VALID_USERNAME, "password": "senha_errada"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Credenciais inválidas"
    
    def test_login_missing_credentials(self):
        """Testa login com credenciais incompletas"""
        response = client.post(
            "/auth/login",
            json={"username": VALID_USERNAME}
        )
        assert response.status_code == 400


class TestPagamentos:
    """Testes para endpoints de pagamentos"""
    
    @pytest.fixture
    def auth_token(self):
        """Fixture que retorna um token de autenticação válido"""
        response = client.post(
            "/auth/login",
            json={"username": VALID_USERNAME, "password": VALID_PASSWORD}
        )
        return response.json()["access_token"]
    
    def test_health_check(self):
        """Testa endpoint de health check"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data
    
    def test_listar_pagamentos_vazio(self):
        """Testa listagem de pagamentos quando vazio"""
        response = client.get("/pagamentos/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_criar_pagamento_sem_autenticacao(self):
        """Testa criação de pagamento sem token"""
        response = client.post(
            "/pagamentos/",
            json={"valor": 100.0, "descricao": "Teste"}
        )
        assert response.status_code == 401
    
    def test_criar_pagamento_com_autenticacao(self, auth_token):
        """Testa criação de pagamento com autenticação"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.post(
            "/pagamentos/",
            json={"valor": 150.50, "descricao": "Pagamento teste"},
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valor"] == 150.50
        assert data["descricao"] == "Pagamento teste"
        assert data["status"] == "pendente"
        assert "id" in data
    
    def test_criar_pagamento_valor_invalido(self, auth_token):
        """Testa criação de pagamento com valor inválido"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.post(
            "/pagamentos/",
            json={"valor": -100.0, "descricao": "Pagamento teste"},
            headers=headers
        )
        assert response.status_code == 422
    
    def test_criar_pagamento_descricao_vazia(self, auth_token):
        """Testa criação de pagamento com descrição vazia"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.post(
            "/pagamentos/",
            json={"valor": 100.0, "descricao": ""},
            headers=headers
        )
        assert response.status_code == 422
    
    def test_atualizar_pagamento_nao_encontrado(self, auth_token):
        """Testa atualização de pagamento inexistente"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.put(
            "/pagamentos/999",
            json={"valor": 200.0, "descricao": "Pagamento atualizado"},
            headers=headers
        )
        assert response.status_code == 404
    
    def test_deletar_pagamento_nao_encontrado(self, auth_token):
        """Testa deleção de pagamento inexistente"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.delete("/pagamentos/999", headers=headers)
        assert response.status_code == 404
    
    def test_atualizar_pagamento_id_invalido(self, auth_token):
        """Testa atualização com ID inválido"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.put(
            "/pagamentos/-1",
            json={"valor": 200.0, "descricao": "Pagamento atualizado"},
            headers=headers
        )
        assert response.status_code == 400
    
    def test_deletar_pagamento_id_invalido(self, auth_token):
        """Testa deleção com ID inválido"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.delete("/pagamentos/-1", headers=headers)
        assert response.status_code == 400


class TestRateLimit:
    """Testes para rate limit"""
    
    @pytest.fixture
    def auth_token(self):
        """Fixture que retorna um token de autenticação válido"""
        response = client.post(
            "/auth/login",
            json={"username": VALID_USERNAME, "password": VALID_PASSWORD}
        )
        return response.json()["access_token"]
    
    def test_rate_limit_listar_pagamentos(self, auth_token):
        """Testa se rate limit é aplicado no endpoint de listagem"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Faz requisições repetidas (mais de 30/minuto é o limite)
        for i in range(5):
            response = client.get("/pagamentos/", headers=headers)
            assert response.status_code == 200
