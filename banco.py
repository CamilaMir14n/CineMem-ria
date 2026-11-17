import sqlite3


class Banco:
    """Cuida da conexão com o SQLite3 e da criação das tabelas."""

    def __init__(self, arquivo="cine_memoria.db"):
        self.arquivo = arquivo
        try:
            # se o arquivo ainda não existir, o SQLite cria na primeira execução
            self.conexao = sqlite3.connect(self.arquivo)
            # no SQLite as chaves estrangeiras vêm desligadas, então ligamos aqui
            self.conexao.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as erro:
            raise ValueError(f"Não foi possível abrir o banco de dados: {erro}")
        self.criar_tabelas()

    def criar_tabelas(self):
        # Tabela 1: filmes e séries (o campo "tipo" diferencia os dois)
        self.executar("""
            CREATE TABLE IF NOT EXISTS conteudos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                tipo TEXT NOT NULL CHECK (tipo IN ('Filme', 'Série')),
                ano INTEGER NOT NULL,
                diretor_criador TEXT,
                duracao INTEGER,
                temporadas INTEGER
            )
        """)

        # Tabela 2: gêneros
        self.executar("""
            CREATE TABLE IF NOT EXISTS generos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            )
        """)

        # Tabela 3: liga conteúdos a gêneros (um conteúdo pode ter vários gêneros)
        self.executar("""
            CREATE TABLE IF NOT EXISTS conteudo_genero (
                conteudo_id INTEGER NOT NULL,
                genero_id INTEGER NOT NULL,
                PRIMARY KEY (conteudo_id, genero_id),
                FOREIGN KEY (conteudo_id) REFERENCES conteudos (id) ON DELETE CASCADE,
                FOREIGN KEY (genero_id) REFERENCES generos (id)
            )
        """)

        # Tabela 4: avaliações (cada conteúdo tem no máximo uma avaliação)
        self.executar("""
            CREATE TABLE IF NOT EXISTS avaliacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conteudo_id INTEGER NOT NULL UNIQUE,
                nota REAL NOT NULL CHECK (nota >= 0 AND nota <= 10),
                comentario TEXT,
                FOREIGN KEY (conteudo_id) REFERENCES conteudos (id) ON DELETE CASCADE
            )
        """)

    def executar(self, sql, parametros=()):
        """Usado para INSERT, UPDATE, DELETE e CREATE. Salva (commit) no final."""
        try:
            cursor = self.conexao.execute(sql, parametros)
            self.conexao.commit()
            return cursor
        except sqlite3.IntegrityError:
            self.conexao.rollback()
            raise ValueError("Os dados não respeitam as regras do banco "
                             "(registro repetido ou em uso por outro registro).")
        except sqlite3.Error as erro:
            self.conexao.rollback()
            raise ValueError(f"Erro no banco de dados: {erro}")

    def consultar(self, sql, parametros=()):
        """Usado para SELECT. Devolve uma lista de tuplas."""
        try:
            return self.conexao.execute(sql, parametros).fetchall()
        except sqlite3.Error as erro:
            raise ValueError(f"Erro ao consultar o banco de dados: {erro}")

    def fechar(self):
        self.conexao.close()
