import sqlite3

from flask import Flask, current_app, g, jsonify, render_template, request


def validar_cliente(dados):
    if not isinstance(dados, dict):
        raise ValueError("Envie os dados do cliente em formato JSON.")
    nome = str(dados.get("nome", "")).strip()
    email = str(dados.get("email", "")).strip()
    if not nome or not email:
        raise ValueError("Nome e e-mail são obrigatórios.")
    return nome, email


def validar_ordem(dados):
    if not isinstance(dados, dict):
        raise ValueError("Envie os dados da ordem em formato JSON.")
    descricao = str(dados.get("descricao", "")).strip()
    cliente_id = dados.get("cliente_id")
    if not descricao or not cliente_id:
        raise ValueError("Cliente e descrição são obrigatórios.")
    try:
        cliente_id = int(cliente_id)
    except (TypeError, ValueError):
        raise ValueError("O ID do cliente deve ser um número inteiro.")
    return cliente_id, descricao


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def fechar_db(_erro=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def inicializar_banco(app):
    with app.app_context():
        db = get_db()
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS ordens_servico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                descricao TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Aberta',
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            );
            """
        )
        db.commit()


def criar_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE="techfix.db",
        TESTING=False,
    )
    if config:
        app.config.update(config)

    app.teardown_appcontext(fechar_db)

    @app.get("/")
    def inicio():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.post("/clientes")
    def criar_cliente():
        try:
            nome, email = validar_cliente(request.get_json(silent=True) or {})
            db = get_db()
            cursor = db.execute(
                "INSERT INTO clientes (nome, email) VALUES (?, ?)",
                (nome, email),
            )
            db.commit()
            return jsonify(
                {"id": cursor.lastrowid, "nome": nome, "email": email}
            ), 201
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        except sqlite3.IntegrityError:
            return jsonify({"erro": "Já existe um cliente com este e-mail."}), 409

    @app.get("/clientes")
    def listar_clientes():
        clientes = get_db().execute(
            "SELECT id, nome, email FROM clientes ORDER BY id"
        ).fetchall()
        return jsonify([dict(cliente) for cliente in clientes]), 200

    @app.post("/os")
    def criar_ordem():
        try:
            cliente_id, descricao = validar_ordem(
                request.get_json(silent=True) or {}
            )
            db = get_db()
            cliente = db.execute(
                "SELECT id FROM clientes WHERE id = ?", (cliente_id,)
            ).fetchone()
            if cliente is None:
                return jsonify({"erro": "Cliente não encontrado."}), 404
            cursor = db.execute(
                "INSERT INTO ordens_servico (cliente_id, descricao) VALUES (?, ?)",
                (cliente_id, descricao),
            )
            db.commit()
            return jsonify(
                {
                    "id": cursor.lastrowid,
                    "cliente_id": cliente_id,
                    "descricao": descricao,
                    "status": "Aberta",
                }
            ), 201
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    @app.get("/os")
    def listar_ordens():
        ordens = get_db().execute(
            """
            SELECT id, cliente_id, descricao, status
            FROM ordens_servico ORDER BY id
            """
        ).fetchall()
        return jsonify([dict(ordem) for ordem in ordens]), 200

    inicializar_banco(app)
    return app
