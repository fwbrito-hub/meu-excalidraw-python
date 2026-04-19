import pytest

def test_status_da_base(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "auth" in response.json()

def test_salvar_projeto_protegido(client):
    """Testa se as rotas de projeto exigem autenticação"""
    
    # 1. Registrar um usuário para este teste especificamente
    user_data = {
        "username": "saveuser",
        "email": "save@example.com",
        "password": "password123"
    }
    client.post("/api/auth/register", json=user_data)
    
    # 2. Login
    login_data = {"username": "saveuser", "password": "password123"}
    resp_token = client.post("/token", data=login_data)
    token = resp_token.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Salvar
    projeto_data = {"nome_projeto": "Teste Protegido", "elementos_json": []}
    response = client.post("/api/projetos/salvar", json=projeto_data, headers=headers)
    assert response.status_code == 200
