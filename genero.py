class Genero:
    """Representa um gênero (ação, comédia, drama...) e faz o CRUD dele."""

    def __init__(self, banco, nome=""):
        self.banco = banco
        self.id = None
        self.nome = nome.strip().title()

    def validar(self):
        if self.nome == "":
            raise ValueError("O nome do gênero não pode ficar vazio.")

    def nome_em_uso(self):
        """Verifica se outro gênero já tem esse nome."""
        linhas = self.banco.consultar("SELECT id FROM generos WHERE nome = ?", (self.nome,))
        for linha in linhas:
            if linha[0] != self.id:
                return True
        return False

    # CREATE
    def inserir(self):
        self.validar()
        if self.nome_em_uso():
            raise ValueError(f"O gênero '{self.nome}' já está cadastrado.")
        cursor = self.banco.executar("INSERT INTO generos (nome) VALUES (?)", (self.nome,))
        self.id = cursor.lastrowid

    # READ
    def listar(self):
        return self.banco.consultar("SELECT id, nome FROM generos ORDER BY nome")

    def buscar(self, codigo):
        linhas = self.banco.consultar("SELECT id, nome FROM generos WHERE id = ?", (codigo,))
        if len(linhas) == 0:
            raise ValueError(f"Não existe gênero com o código {codigo}.")
        return linhas[0]

    # UPDATE
    def atualizar(self):
        self.validar()
        self.buscar(self.id)
        if self.nome_em_uso():
            raise ValueError(f"Já existe outro gênero chamado '{self.nome}'.")
        self.banco.executar("UPDATE generos SET nome = ? WHERE id = ?", (self.nome, self.id))

    # DELETE
    def excluir(self):
        self.buscar(self.id)
        linhas = self.banco.consultar(
            "SELECT COUNT(*) FROM conteudo_genero WHERE genero_id = ?", (self.id,))
        quantidade = linhas[0][0]
        if quantidade > 0:
            raise ValueError(f"Este gênero está em uso por {quantidade} título(s). "
                             "Retire o gênero desses títulos antes de excluir.")
        self.banco.executar("DELETE FROM generos WHERE id = ?", (self.id,))
