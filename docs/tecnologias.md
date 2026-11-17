# Tecnologias e arquitetura — TechFix

## Arquitetura
O projeto adota arquitetura monolítica organizada em camadas, mantendo separadas as rotas, regras de aplicação, modelos de dados e apresentação.

## Tecnologias previstas
- Python: linguagem principal.
- Flask: framework web.
- Jinja2: renderização de páginas HTML.
- Bootstrap 5.3: componentes e responsividade da interface.
- SQLite: banco de dados relacional leve.
- Flask-SQLAlchemy: mapeamento objeto-relacional.

## Segurança
As senhas não devem ser armazenadas em texto puro. A autenticação deverá utilizar hash apropriado, como scrypt ou PBKDF2. As entradas devem ser validadas e as rotas protegidas contra acesso não autorizado.

## Qualidade
O desenvolvimento deverá incluir testes automatizados para as funcionalidades principais e integração contínua para executar verificações a cada atualização do repositório.