# Estrutura inicial do projeto

A aplicação será organizada para separar responsabilidades e facilitar manutenção.

```text
techfix-mvp/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── templates/
│   └── static/
├── tests/
├── docs/
├── config.py
├── run.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Responsabilidades
- `app/models/`: entidades e persistência dos dados.
- `app/routes/`: rotas e controladores da aplicação.
- `app/templates/`: páginas HTML renderizadas pelo Jinja2.
- `app/static/`: arquivos CSS, JavaScript e imagens.
- `tests/`: testes automatizados.
- `docs/`: documentação técnica e requisitos.
- `config.py`: configurações da aplicação.
- `run.py`: ponto de inicialização do servidor.