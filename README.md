# TechFix — Gestão de Assistência Técnica

MVP web para cadastro de clientes, abertura e consulta de ordens de serviço.

## Executar localmente

1. Instale Python 3.10 ou superior.
2. No terminal, dentro da pasta do projeto, execute:

```bash
python -m venv .venv
```

No Windows:

```powershell
.venv\\Scripts\\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

3. Instale as dependências e inicie a aplicação:

```bash
python -m pip install -r requirements.txt
flask --app app:criar_app run --debug
```

4. Acesse http://127.0.0.1:5000.

O banco SQLite `techfix.db` é criado automaticamente. A tela inicial permite cadastrar clientes e registrar/consultar ordens de serviço. O botão **Alto contraste** ativa uma apresentação de alto contraste, e a preferência fica salva no navegador.

## Testes

```bash
pytest -v --cov=app --cov-report=term-missing
```

O GitHub Actions executa os testes automaticamente em pushes e pull requests.
