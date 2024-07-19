from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def teste_deve_criar_conta_distribuidora():
    nova_conta = {
        "idade": 21,
        "endereco": "rua macapa 246",
        "telefone": "11999999999",
        "status_atividade": True,
        "cpf": "12345678901"

    }
    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["nome"] = "jorge"
    response = client.post("/distribuidora", json=nova_conta)
    assert response.status_code == 201
    assert response.json() == nova_conta_copy

    print(response.json())





