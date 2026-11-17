import pytest

from app import criar_app, inicializar_banco


@pytest.fixture
def app(tmp_path):
    banco = tmp_path / "techfix_teste.db"
    aplicacao = criar_app(
        {
            "TESTING": True,
            "DATABASE": str(banco),
        }
    )
    inicializar_banco(aplicacao)
    yield aplicacao


@pytest.fixture
def client(app):
    return app.test_client()
