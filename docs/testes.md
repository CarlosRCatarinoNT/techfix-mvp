# Testes automatizados e integração contínua

O projeto utiliza `pytest` para testes unitários e de integração e `pytest-cov` para medir a cobertura do módulo `app.py`.

## Executar localmente

```bash
python -m pip install -r requirements.txt
pytest -v --cov=app --cov-report=term-missing
```

Os testes unitários verificam as funções de validação de clientes e ordens de serviço. Os testes de integração exercitam as rotas Flask e a persistência em um banco SQLite temporário.

O workflow em `.github/workflows/tests.yml` executa os mesmos testes automaticamente em pushes na branch principal/de funcionalidades e em pull requests direcionados à branch principal. O resultado e a cobertura são exibidos no log do GitHub Actions.
