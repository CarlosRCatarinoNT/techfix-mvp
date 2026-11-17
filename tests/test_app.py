import pytest

from app import validar_cliente, validar_ordem


# Testes unitários: validam as funções de validação isoladamente.
def test_validar_cliente_retorna_dados_limpos():
    assert validar_cliente({"nome": " Ana ", "email": " ana@email.com "}) == (
        "Ana",
        "ana@email.com",
    )


def test_validar_cliente_rejeita_campos_obrigatorios():
    with pytest.raises(ValueError):
        validar_cliente({"nome": "", "email": ""})


def test_validar_cliente_rejeita_formato_invalido():
    with pytest.raises(ValueError):
        validar_cliente(["Ana", "ana@email.com"])


def test_validar_ordem_retorna_dados_validos():
    assert validar_ordem({"cliente_id": "1", "descricao": "Conserto"}) == (
        1,
        "Conserto",
    )


def test_validar_ordem_rejeita_id_invalido():
    with pytest.raises(ValueError):
        validar_ordem({"cliente_id": "abc", "descricao": "Conserto"})


def test_validar_ordem_rejeita_dados_incompletos():
    with pytest.raises(ValueError):
        validar_ordem({"cliente_id": 1, "descricao": ""})


# Testes de integração: validam rotas, persistência e comunicação com SQLite.
def test_health(client):
    resposta = client.get("/health")
    assert resposta.status_code == 200
    assert resposta.json == {"status": "ok"}


def test_criar_e_listar_cliente(client):
    criado = client.post(
        "/clientes",
        json={"nome": "Ana", "email": "ana@email.com"},
    )
    assert criado.status_code == 201
    assert criado.json["id"] == 1

    listado = client.get("/clientes")
    assert listado.status_code == 200
    assert listado.json == [
        {"id": 1, "nome": "Ana", "email": "ana@email.com"}
    ]


def test_cliente_com_dados_invalidos(client):
    resposta = client.post("/clientes", json={"nome": "", "email": ""})
    assert resposta.status_code == 400
    assert "erro" in resposta.json


def test_cliente_com_email_duplicado(client):
    dados = {"nome": "Ana", "email": "ana@email.com"}
    assert client.post("/clientes", json=dados).status_code == 201
    duplicado = client.post("/clientes", json=dados)
    assert duplicado.status_code == 409


def test_criar_e_listar_ordem_de_servico(client):
    cliente = client.post(
        "/clientes",
        json={"nome": "Ana", "email": "ana@email.com"},
    )
    ordem = client.post(
        "/os",
        json={"cliente_id": cliente.json["id"], "descricao": "Troca de tela"},
    )
    assert ordem.status_code == 201
    assert ordem.json["status"] == "Aberta"

    listado = client.get("/os")
    assert listado.status_code == 200
    assert listado.json[0]["descricao"] == "Troca de tela"


def test_ordem_com_dados_invalidos(client):
    resposta = client.post("/os", json={"cliente_id": 1, "descricao": ""})
    assert resposta.status_code == 400


def test_ordem_para_cliente_inexistente(client):
    resposta = client.post(
        "/os",
        json={"cliente_id": 999, "descricao": "Diagnóstico"},
    )
    assert resposta.status_code == 404


def test_listagens_vazias(client):
    assert client.get("/clientes").json == []
    assert client.get("/os").json == []


def test_pagina_inicial_exibe_interface_acessivel(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert b"TechFix" in resposta.data
    assert b"contrast-toggle" in resposta.data
    assert b"aria-live" in resposta.data
