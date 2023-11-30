from sys import exit
from pathlib import Path

from .parser_model import Parser


class Program:
    def read_file(file_name):
        file_dir = Path(__file__).parent.parent.joinpath("public")
        desired_file = file_dir.joinpath(file_dir, file_name)

        try:
            with open(desired_file) as file:
                mini_pascal_code = file.readlines()
                mini_pascal_code = " ".join(mini_pascal_code)
                mini_pascal_code = mini_pascal_code + " "
        except FileNotFoundError:
            print(f"O arquivo {file_name} não existe.")
            exit(0)

        return mini_pascal_code

    @staticmethod
    def execute():
        should_exit = False

        print("1 - Compilar arquivo TXT contendo um código em mini-pascal")
        print("2 - Compilar o arquivo de exemplo (teste.txt)")
        print("0 - Sair do programa")
        opcao = input("\nSelecione uma opção: ")

        match opcao:
            case "1":
                file_name = input(
                    "Digite o nome do arquivo (IMPORTANTE!!! o arquivo deve estar na pasta public): "
                )

                if file_name.endswith(".txt"):
                    codigo = Program.read_file(file_name)
                else:
                    err_msg = "O arquivo " + file_name + " não é do tipo TXT!!!"
                    print(err_msg)
                    should_exit = True
            case "2":
                codigo = Program.read_file("teste18.txt")
            case "0":
                should_exit = True
            case _:
                print("Opção indisponível!")
                should_exit = True

        if should_exit is False:
            Parser(codigo, iu=False).parse()
        else:
            print("Interrompendo programa...")
            exit(0)
