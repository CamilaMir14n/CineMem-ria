class Avaliacao:
    """Representa a nota (0 a 10) e o comentário de um filme ou série."""

    def __init__(self, banco, conteudo_id=None, nota=None, comentario=""):
        self.banco = banco
        self.id = None
        self.conteudo_id = conteudo_id
        self.nota = nota
        self.comentario = comentario.strip()

    def validar(self):
        if self.nota is None or not (0 <= self.nota <= 10):
            raise ValueError("A nota deve estar entre 0 e 10.")

    # CREATE
    def inserir(self):
        self.validar()
        titulo = self.banco.consultar("SELECT id FROM conteudos WHERE id = ?", (self.conteudo_id,))
        if len(titulo) == 0:
            raise ValueError(f"Não existe título com o código {self.conteudo_id}.")
        ja_avaliado = self.banco.consultar(
            "SELECT id FROM avaliacoes WHERE conteudo_id = ?", (self.conteudo_id,))
        if len(ja_avaliado) > 0:
            raise ValueError("Este título já foi avaliado. Use a opção de atualizar a avaliação.")
        cursor = self.banco.executar(
            "INSERT INTO avaliacoes (conteudo_id, nota, comentario) VALUES (?, ?, ?)",
            (self.conteudo_id, self.nota, self.comentario))
        self.id = cursor.lastrowid

    # READ
    def listar(self):
        return self.banco.consultar(
            "SELECT a.id, a.conteudo_id, c.titulo, c.tipo, a.nota, a.comentario "
            "FROM avaliacoes a JOIN conteudos c ON c.id = a.conteudo_id "
            "ORDER BY c.titulo COLLATE NOCASE")

    def buscar(self, codigo):
        linhas = self.banco.consultar(
            "SELECT a.id, a.conteudo_id, c.titulo, c.tipo, a.nota, a.comentario "
            "FROM avaliacoes a JOIN conteudos c ON c.id = a.conteudo_id "
            "WHERE a.id = ?", (codigo,))
        if len(linhas) == 0:
            raise ValueError(f"Não existe avaliação com o código {codigo}.")
        return linhas[0]

    # UPDATE
    def atualizar(self):
        self.validar()
        self.buscar(self.id)
        self.banco.executar("UPDATE avaliacoes SET nota = ?, comentario = ? WHERE id = ?",
                            (self.nota, self.comentario, self.id))

    # DELETE
    def excluir(self):
        self.buscar(self.id)
        self.banco.executar("DELETE FROM avaliacoes WHERE id = ?", (self.id,))
