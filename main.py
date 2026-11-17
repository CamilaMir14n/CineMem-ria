from banco import Banco
from menu import Menu


def main():
    try:
        banco = Banco()
    except ValueError as erro:
        print(erro)
        return

    menu = Menu(banco)
    try:
        menu.iniciar()
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma encerrado pelo usuário.")
    finally:
        banco.fechar()
        print("Banco de dados fechado.")


if __name__ == "__main__":
    main()
