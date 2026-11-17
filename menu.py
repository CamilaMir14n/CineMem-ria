from conteudo import Conteudo
from genero import Genero
from avaliacao import Avaliacao


class Menu:
    """Mostra os menus no terminal e chama as classes do sistema."""

    def __init__(self, banco):
        self.banco = banco
        # objetos usados para as consultas (listagens)
        self.conteudo = Conteudo(banco)
        self.genero = Genero(banco)
        self.avaliacao = Avaliacao(banco)

    # ------------------------------------------------------------------
    # Funções de leitura (repetem até o usuário digitar algo válido)
    # ------------------------------------------------------------------
    def ler_inteiro(self, texto, minimo, maximo, atual=None):
        """Lê um número inteiro entre minimo e maximo.
        Se 'atual' for informado, deixar em branco mantém o valor atual."""
        while True:
            resposta = input(texto).strip()
            if resposta == "" and atual is not None:
                return atual
            try:
                valor = int(resposta)
            except ValueError:
                print("Digite apenas números inteiros.")
            else:
                if valor < minimo or valor > maximo:
                    print(f"Digite um valor entre {minimo} e {maximo}.")
                else:
                    return valor

    def ler_codigo(self, texto):
        """Lê um código. O valor 0 serve para cancelar."""
        return self.ler_inteiro(texto + " (0 para cancelar): ", 0, 999999)

    def ler_nota(self, texto, atual=None):
        while True:
            resposta = input(texto).strip().replace(",", ".")
            if resposta == "" and atual is not None:
                return atual
            try:
                nota = float(resposta)
            except ValueError:
                print("Digite um número, por exemplo 8 ou 7.5.")
            else:
                if not (0 <= nota <= 10):
                    print("A nota deve estar entre 0 e 10.")
                else:
                    return nota

    def confirmar(self, pergunta):
        resposta = input(f"{pergunta} (s/n): ").strip().lower()
        return resposta == "s" or resposta == "sim"

    # ------------------------------------------------------------------
    # Funções que mostram dados na tela
    # ------------------------------------------------------------------
    def exibir_titulos(self, linhas):
        if len(linhas) == 0:
            print("\nNenhum título encontrado.")
            return
        print()
        for linha in linhas:
            codigo, tipo, titulo, ano, diretor, duracao, temporadas, nota = linha
            generos = self.conteudo.buscar_generos(codigo)

            if tipo == "Filme":
                rotulo = "Diretor"
                detalhe = f"Duração: {duracao} min"
            else:
                rotulo = "Criador"
                detalhe = f"Temporadas: {temporadas}"

            if diretor is None or diretor == "":
                diretor = "não informado"
            if len(generos) == 0:
                texto_generos = "nenhum"
            else:
                texto_generos = ", ".join(generos)
            if nota is None:
                texto_nota = "sem avaliação"
            else:
                texto_nota = f"{nota:g}/10"

            print(f"[{codigo}] {tipo} - {titulo} ({ano})")
            print(f"     {rotulo}: {diretor} | {detalhe}")
            print(f"     Gêneros: {texto_generos} | Nota: {texto_nota}")
            print("-" * 40)
        print(f"Total: {len(linhas)} título(s).")

    def exibir_generos(self, linhas):
        if len(linhas) == 0:
            print("\nNenhum gênero cadastrado.")
            return
        print()
        for linha in linhas:
            print(f"[{linha[0]}] {linha[1]}")
        print(f"Total: {len(linhas)} gênero(s).")

    def exibir_avaliacoes(self, linhas):
        if len(linhas) == 0:
            print("\nNenhuma avaliação registrada.")
            return
        print()
        for linha in linhas:
            codigo, conteudo_id, titulo, tipo, nota, comentario = linha
            if comentario is None or comentario == "":
                comentario = "(sem comentário)"
            print(f"[Avaliação {codigo}] {tipo} - {titulo}")
            print(f"     Nota: {nota:g}/10")
            print(f"     Comentário: {comentario}")
            print("-" * 40)
        print(f"Total: {len(linhas)} avaliação(ões).")

    def exibir_titulos_resumo(self, linhas):
        """Lista mais curta, usada nas consultas de títulos avaliados."""
        if len(linhas) == 0:
            print("\nNenhum título avaliado.")
            return
        print()
        for linha in linhas:
            print(f"[{linha[0]}] {linha[1]} - {linha[2]} ({linha[3]}) - Nota: {linha[4]:g}/10")
        print(f"Total: {len(linhas)} título(s) avaliado(s).")

    # ------------------------------------------------------------------
    # Menu principal
    # ------------------------------------------------------------------
    def iniciar(self):
        opcao = ""
        while opcao != "0":
            print("\n" + "=" * 40)
            print("             CINEMEMÓRIA")
            print("       Sua coleção de histórias")
            print("=" * 40)
            print("\n1 - Gerenciar filmes e séries")
            print("2 - Gerenciar gêneros")
            print("3 - Gerenciar avaliações")
            print("4 - Consultas")
            print("0 - Sair")

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "1":
                self.menu_titulos()
            elif opcao == "2":
                self.menu_generos()
            elif opcao == "3":
                self.menu_avaliacoes()
            elif opcao == "4":
                self.menu_consultas()
            elif opcao == "0":
                print("\nAté a próxima!")
            else:
                print("\nOpção inválida! Escolha um número de 0 a 4.")

    # ------------------------------------------------------------------
    # 1 - Filmes e séries
    # ------------------------------------------------------------------
    def menu_titulos(self):
        opcao = ""
        while opcao != "0":
            print("\n--- FILMES E SÉRIES ---")
            print("1 - Cadastrar filme")
            print("2 - Cadastrar série")
            print("3 - Listar todos os títulos")
            print("4 - Pesquisar título pelo nome")
            print("5 - Atualizar um título")
            print("6 - Excluir um título")
            print("7 - Definir os gêneros de um título")
            print("0 - Voltar")

            opcao = input("\nEscolha uma opção: ").strip()

            try:
                if opcao == "1":
                    self.cadastrar_titulo("Filme")
                elif opcao == "2":
                    self.cadastrar_titulo("Série")
                elif opcao == "3":
                    self.exibir_titulos(self.conteudo.listar())
                elif opcao == "4":
                    self.pesquisar_titulo()
                elif opcao == "5":
                    self.atualizar_titulo()
                elif opcao == "6":
                    self.excluir_titulo()
                elif opcao == "7":
                    self.definir_generos_titulo()
                elif opcao != "0":
                    print("\nOpção inválida! Escolha um número de 0 a 7.")
            except ValueError as erro:
                print(f"\nAtenção: {erro}")

    def cadastrar_titulo(self, tipo):
        print(f"\n--- Cadastrar {tipo.lower()} ---")
        titulo = input("Título: ")
        ano = self.ler_inteiro("Ano de lançamento: ", 1888, 2100)

        duracao = None
        temporadas = None
        if tipo == "Filme":
            diretor = input("Diretor (opcional): ")
            duracao = self.ler_inteiro("Duração em minutos: ", 1, 1000)
        else:
            diretor = input("Criador (opcional): ")
            temporadas = self.ler_inteiro("Número de temporadas: ", 1, 100)

        novo = Conteudo(self.banco, titulo, tipo, ano, diretor, duracao, temporadas)
        novo.inserir()
        print(f"\nCadastro realizado com sucesso! Código: {novo.id}")

        if self.confirmar("Deseja escolher os gêneros agora?"):
            self.escolher_generos(novo)

    def escolher_generos(self, conteudo):
        """Pergunta os códigos dos gêneros e salva no título."""
        generos = self.genero.listar()
        if len(generos) == 0:
            print("\nNenhum gênero cadastrado. Cadastre gêneros no menu 'Gerenciar gêneros'.")
            return
        self.exibir_generos(generos)
        texto = input("\nDigite os códigos dos gêneros separados por vírgula (Enter = nenhum): ")

        codigos = []
        for parte in texto.split(","):
            parte = parte.strip()
            if parte == "":
                continue
            if not parte.isdigit():
                raise ValueError(f"'{parte}' não é um código válido.")
            if int(parte) not in codigos:
                codigos.append(int(parte))

        conteudo.definir_generos(codigos)
        print("Gêneros do título atualizados com sucesso!")

    def escolher_titulo(self):
        """Mostra os títulos e pede um código. Devolve a linha do título (ou None se cancelar)."""
        linhas = self.conteudo.listar()
        if len(linhas) == 0:
            print("\nNenhum título cadastrado.")
            return None
        self.exibir_titulos(linhas)
        codigo = self.ler_codigo("\nCódigo do título")
        if codigo == 0:
            print("Operação cancelada.")
            return None
        return self.conteudo.buscar(codigo)

    def pesquisar_titulo(self):
        texto = input("\nDigite parte do nome do título: ")
        if texto.strip() == "":
            raise ValueError("Digite pelo menos uma letra para pesquisar.")
        self.exibir_titulos(self.conteudo.pesquisar(texto))

    def atualizar_titulo(self):
        print("\n--- Atualizar título ---")
        linha = self.escolher_titulo()
        if linha is None:
            return
        codigo, tipo, titulo_atual, ano_atual, diretor_atual, duracao_atual, temporadas_atual = linha

        print("\nDeixe em branco para manter o valor atual.")
        titulo = input(f"Título [{titulo_atual}]: ").strip()
        if titulo == "":
            titulo = titulo_atual
        ano = self.ler_inteiro(f"Ano de lançamento [{ano_atual}]: ", 1888, 2100, ano_atual)

        if diretor_atual is None:
            diretor_atual = ""
        duracao = None
        temporadas = None
        if tipo == "Filme":
            diretor = input(f"Diretor [{diretor_atual}]: ").strip()
            duracao = self.ler_inteiro(f"Duração em minutos [{duracao_atual}]: ", 1, 1000, duracao_atual)
        else:
            diretor = input(f"Criador [{diretor_atual}]: ").strip()
            temporadas = self.ler_inteiro(f"Temporadas [{temporadas_atual}]: ", 1, 100, temporadas_atual)
        if diretor == "":
            diretor = diretor_atual

        alterado = Conteudo(self.banco, titulo, tipo, ano, diretor, duracao, temporadas)
        alterado.id = codigo
        alterado.atualizar()
        print("\nTítulo atualizado com sucesso!")

    def excluir_titulo(self):
        print("\n--- Excluir título ---")
        linha = self.escolher_titulo()
        if linha is None:
            return
        print(f"\nVocê vai excluir: {linha[1]} - {linha[2]} ({linha[3]})")
        print("A avaliação e os gêneros ligados a ele também serão apagados.")
        if self.confirmar("Tem certeza?"):
            apagar = Conteudo(self.banco)
            apagar.id = linha[0]
            apagar.excluir()
            print("\nTítulo excluído com sucesso!")
        else:
            print("Exclusão cancelada.")

    def definir_generos_titulo(self):
        print("\n--- Definir gêneros de um título ---")
        linha = self.escolher_titulo()
        if linha is None:
            return
        alvo = Conteudo(self.banco)
        alvo.id = linha[0]
        atuais = alvo.buscar_generos(alvo.id)
        if len(atuais) == 0:
            print("\nGêneros atuais: nenhum")
        else:
            print(f"\nGêneros atuais: {', '.join(atuais)}")
        print("Os gêneros que você escolher agora substituem os atuais.")
        self.escolher_generos(alvo)

    # ------------------------------------------------------------------
    # 2 - Gêneros
    # ------------------------------------------------------------------
    def menu_generos(self):
        opcao = ""
        while opcao != "0":
            print("\n--- GÊNEROS ---")
            print("1 - Cadastrar gênero")
            print("2 - Listar gêneros")
            print("3 - Atualizar gênero")
            print("4 - Excluir gênero")
            print("0 - Voltar")

            opcao = input("\nEscolha uma opção: ").strip()

            try:
                if opcao == "1":
                    self.cadastrar_genero()
                elif opcao == "2":
                    self.exibir_generos(self.genero.listar())
                elif opcao == "3":
                    self.atualizar_genero()
                elif opcao == "4":
                    self.excluir_genero()
                elif opcao != "0":
                    print("\nOpção inválida! Escolha um número de 0 a 4.")
            except ValueError as erro:
                print(f"\nAtenção: {erro}")

    def cadastrar_genero(self):
        print("\n--- Cadastrar gênero ---")
        nome = input("Nome do gênero (ex: Ação, Comédia, Terror): ")
        novo = Genero(self.banco, nome)
        novo.inserir()
        print(f"\nGênero '{novo.nome}' cadastrado com sucesso! Código: {novo.id}")

    def escolher_genero(self):
        """Mostra os gêneros e pede um código. Devolve a linha do gênero (ou None se cancelar)."""
        linhas = self.genero.listar()
        if len(linhas) == 0:
            print("\nNenhum gênero cadastrado.")
            return None
        self.exibir_generos(linhas)
        codigo = self.ler_codigo("\nCódigo do gênero")
        if codigo == 0:
            print("Operação cancelada.")
            return None
        return self.genero.buscar(codigo)

    def atualizar_genero(self):
        print("\n--- Atualizar gênero ---")
        linha = self.escolher_genero()
        if linha is None:
            return
        nome = input(f"Novo nome [{linha[1]}]: ")
        alterado = Genero(self.banco, nome)
        alterado.id = linha[0]
        alterado.atualizar()
        print("\nGênero atualizado com sucesso!")

    def excluir_genero(self):
        print("\n--- Excluir gênero ---")
        linha = self.escolher_genero()
        if linha is None:
            return
        if self.confirmar(f"Excluir o gênero '{linha[1]}'?"):
            apagar = Genero(self.banco)
            apagar.id = linha[0]
            apagar.excluir()
            print("\nGênero excluído com sucesso!")
        else:
            print("Exclusão cancelada.")

    # ------------------------------------------------------------------
    # 3 - Avaliações
    # ------------------------------------------------------------------
    def menu_avaliacoes(self):
        opcao = ""
        while opcao != "0":
            print("\n--- AVALIAÇÕES ---")
            print("1 - Registrar avaliação")
            print("2 - Consultar avaliações")
            print("3 - Atualizar avaliação")
            print("4 - Excluir avaliação")
            print("0 - Voltar")

            opcao = input("\nEscolha uma opção: ").strip()

            try:
                if opcao == "1":
                    self.registrar_avaliacao()
                elif opcao == "2":
                    self.exibir_avaliacoes(self.avaliacao.listar())
                elif opcao == "3":
                    self.atualizar_avaliacao()
                elif opcao == "4":
                    self.excluir_avaliacao()
                elif opcao != "0":
                    print("\nOpção inválida! Escolha um número de 0 a 4.")
            except ValueError as erro:
                print(f"\nAtenção: {erro}")

    def registrar_avaliacao(self):
        print("\n--- Registrar avaliação ---")
        linha = self.escolher_titulo()
        if linha is None:
            return
        print(f"\nAvaliando: {linha[1]} - {linha[2]} ({linha[3]})")
        nota = self.ler_nota("Nota de 0 a 10: ")
        comentario = input("Comentário pessoal (opcional): ")

        nova = Avaliacao(self.banco, linha[0], nota, comentario)
        nova.inserir()
        print(f"\nAvaliação registrada com sucesso! Código: {nova.id}")

    def escolher_avaliacao(self):
        """Mostra as avaliações e pede um código. Devolve a linha (ou None se cancelar)."""
        linhas = self.avaliacao.listar()
        if len(linhas) == 0:
            print("\nNenhuma avaliação registrada.")
            return None
        self.exibir_avaliacoes(linhas)
        codigo = self.ler_codigo("\nCódigo da avaliação")
        if codigo == 0:
            print("Operação cancelada.")
            return None
        return self.avaliacao.buscar(codigo)

    def atualizar_avaliacao(self):
        print("\n--- Atualizar avaliação ---")
        linha = self.escolher_avaliacao()
        if linha is None:
            return
        codigo, conteudo_id, titulo, tipo, nota_atual, comentario_atual = linha
        if comentario_atual is None:
            comentario_atual = ""

        print("\nDeixe em branco para manter o valor atual (no comentário, digite - para apagar).")
        nota = self.ler_nota(f"Nota [{nota_atual:g}]: ", nota_atual)
        comentario = input(f"Comentário [{comentario_atual}]: ").strip()
        if comentario == "":
            comentario = comentario_atual
        elif comentario == "-":
            comentario = ""

        alterada = Avaliacao(self.banco, conteudo_id, nota, comentario)
        alterada.id = codigo
        alterada.atualizar()
        print("\nAvaliação atualizada com sucesso!")

    def excluir_avaliacao(self):
        print("\n--- Excluir avaliação ---")
        linha = self.escolher_avaliacao()
        if linha is None:
            return
        if self.confirmar(f"Excluir a avaliação de '{linha[2]}'?"):
            apagar = Avaliacao(self.banco)
            apagar.id = linha[0]
            apagar.excluir()
            print("\nAvaliação excluída com sucesso!")
        else:
            print("Exclusão cancelada.")

    # ------------------------------------------------------------------
    # 4 - Consultas
    # ------------------------------------------------------------------
    def menu_consultas(self):
        opcao = ""
        while opcao != "0":
            print("\n--- CONSULTAS ---")
            print("1 - Listar todos os filmes")
            print("2 - Listar todas as séries")
            print("3 - Listar títulos por gênero")
            print("4 - Consultar títulos avaliados")
            print("5 - Consultar avaliações e comentários")
            print("6 - Pesquisar título pelo nome")
            print("0 - Voltar")

            opcao = input("\nEscolha uma opção: ").strip()

            try:
                if opcao == "1":
                    self.exibir_titulos(self.conteudo.listar("Filme"))
                elif opcao == "2":
                    self.exibir_titulos(self.conteudo.listar("Série"))
                elif opcao == "3":
                    self.consultar_por_genero()
                elif opcao == "4":
                    self.exibir_titulos_resumo(self.conteudo.listar_avaliados())
                elif opcao == "5":
                    self.exibir_avaliacoes(self.avaliacao.listar())
                elif opcao == "6":
                    self.pesquisar_titulo()
                elif opcao != "0":
                    print("\nOpção inválida! Escolha um número de 0 a 6.")
            except ValueError as erro:
                print(f"\nAtenção: {erro}")

    def consultar_por_genero(self):
        print("\n--- Títulos por gênero ---")
        linha = self.escolher_genero()
        if linha is None:
            return
        print(f"\nTítulos do gênero {linha[1]}:")
        self.exibir_titulos(self.conteudo.listar_por_genero(linha[0]))
