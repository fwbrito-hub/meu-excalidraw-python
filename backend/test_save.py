import requests

r = requests.post(
    "http://localhost:8000/api/projetos/salvar",
    headers={"Authorization": "Bearer dev-admin-token", "Content-Type": "application/json"},
    json={"nome_projeto": "Teste_CLI", "elementos_json": [{"type": "rectangle", "x": 100, "y": 100}]}
)
print(f"Status: {r.status_code}")
print(f"Headers: {dict(r.headers)}")
print(f"Body text: '{r.text}'")
