class Conteudo:
    """Representa um filme ou uma série e faz o CRUD dele."""

    def __init__(self, banco, titulo="", tipo="", ano=0, diretor="", duracao=None, temporadas=None):
        self.banco = banco
        self.id = None
        self.titulo = titulo.strip()
        self.tipo = tipo              # "Filme" ou "Série"
        self.ano = ano
        self.diretor = diretor.strip()  # diretor (filme) ou criador (série)
        self.duracao = duracao        # em minutos, só para filmes
        self.temporadas = temporadas  # só para séries

    def validar(self):
        if self.titulo == "":
            raise ValueError("O título não pode ficar vazio.")
        if self.tipo != "Filme" and self.tipo != "Série":
            raise ValueError("O tipo deve ser Filme ou Série.")
        if self.ano < 1888 or self.ano > 2100:
            raise ValueError("Informe um ano de lançamento entre 1888 e 2100.")
        if self.tipo == "Filme":
            if self.duracao is None or self.duracao <= 0:
                raise ValueError("A duração do filme deve ser maior que zero.")
        else:
            if self.temporadas is None or self.temporadas < 1:
                raise ValueError("A série deve ter pelo menos 1 temporada.")

    def ja_existe(self):
        """Verifica se já existe outro registro com mesmo título, tipo e ano."""
        for linha in self.listar():
            mesmo_titulo = linha[2].lower() == self.titulo.lower()
            if mesmo_titulo and linha[1] == self.tipo and linha[3] == self.ano and linha[0] != self.id:
                return True
        return False

    # CREATE
    def inserir(self):
        self.validar()
        if self.ja_existe():
            raise ValueError(f"{self.tipo} '{self.titulo}' ({self.ano}) já está cadastrado.")
        cursor = self.banco.executar(
            "INSERT INTO conteudos (titulo, tipo, ano, diretor_criador, duracao, temporadas) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (self.titulo, self.tipo, self.ano, self.diretor, self.duracao, self.temporadas))
        self.id = cursor.lastrowid

    # READ
    def buscar(self, codigo):
        linhas = self.banco.consultar(
            "SELECT id, tipo, titulo, ano, diretor_criador, duracao, temporadas "
            "FROM conteudos WHERE id = ?", (codigo,))
        if len(linhas) == 0:
            raise ValueError(f"Não existe título com o código {codigo}.")
        return linhas[0]

    def listar(self, tipo=None):
        """Lista todos os títulos (ou só filmes / só séries) junto com a nota, se houver."""
        sql = ("SELECT c.id, c.tipo, c.titulo, c.ano, c.diretor_criador, c.duracao, "
               "c.temporadas, a.nota "
               "FROM conteudos c LEFT JOIN avaliacoes a ON a.conteudo_id = c.id")
        if tipo is None:
            return self.banco.consultar(sql + " ORDER BY c.titulo COLLATE NOCASE")
        return self.banco.consultar(sql + " WHERE c.tipo = ? ORDER BY c.titulo COLLATE NOCASE", (tipo,))

    def pesquisar(self, texto):
        """Procura títulos que contenham o texto digitado (sem diferenciar maiúsculas)."""
        encontrados = []
        for linha in self.listar():
            if texto.strip().lower() in linha[2].lower():
                encontrados.append(linha)
        return encontrados

    def listar_por_genero(self, genero_id):
        return self.banco.consultar(
            "SELECT c.id, c.tipo, c.titulo, c.ano, c.diretor_criador, c.duracao, "
            "c.temporadas, a.nota "
            "FROM conteudos c "
            "JOIN conteudo_genero cg ON cg.conteudo_id = c.id "
            "LEFT JOIN avaliacoes a ON a.conteudo_id = c.id "
            "WHERE cg.genero_id = ? ORDER BY c.titulo COLLATE NOCASE", (genero_id,))

    def listar_avaliados(self):
        return self.banco.consultar(
            "SELECT c.id, c.tipo, c.titulo, c.ano, a.nota "
            "FROM conteudos c JOIN avaliacoes a ON a.conteudo_id = c.id "
            "ORDER BY a.nota DESC, c.titulo COLLATE NOCASE")

    def buscar_generos(self, codigo):
        """Devolve uma lista com os nomes dos gêneros de um título."""
        linhas = self.banco.consultar(
            "SELECT g.nome FROM generos g "
            "JOIN conteudo_genero cg ON cg.genero_id = g.id "
            "WHERE cg.conteudo_id = ? ORDER BY g.nome", (codigo,))
        nomes = []
        for linha in linhas:
            nomes.append(linha[0])
        return nomes

    # UPDATE
    def atualizar(self):
        self.validar()
        self.buscar(self.id)
        if self.ja_existe():
            raise ValueError(f"Já existe outro registro de {self.tipo} chamado "
                             f"'{self.titulo}' ({self.ano}).")
        self.banco.executar(
            "UPDATE conteudos SET titulo = ?, ano = ?, diretor_criador = ?, "
            "duracao = ?, temporadas = ? WHERE id = ?",
            (self.titulo, self.ano, self.diretor, self.duracao, self.temporadas, self.id))

    def definir_generos(self, lista_ids):
        """Troca os gêneros do título pelos códigos da lista."""
        self.buscar(self.id)
        for genero_id in lista_ids:
            linhas = self.banco.consultar("SELECT id FROM generos WHERE id = ?", (genero_id,))
            if len(linhas) == 0:
                raise ValueError(f"Não existe gênero com o código {genero_id}.")
        self.banco.executar("DELETE FROM conteudo_genero WHERE conteudo_id = ?", (self.id,))
        for genero_id in lista_ids:
            self.banco.executar(
                "INSERT INTO conteudo_genero (conteudo_id, genero_id) VALUES (?, ?)",
                (self.id, genero_id))

    # DELETE
    def excluir(self):
        self.buscar(self.id)
        # os vínculos com gêneros e a avaliação são apagados junto (ON DELETE CASCADE)
        self.banco.executar("DELETE FROM conteudos WHERE id = ?", (self.id,))
