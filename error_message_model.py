class ErrorMessage:
    def __init__(self, erro, linha, coluna, elemento):
        self.erro = erro
        self.linha = linha
        self.coluna = coluna
        self.elemento = elemento
        self.lst_erro = [
            "program",  # 1
            "identificador",  # 2
            ";",  # 3
            "var",  # 4
            ": e um identificador",  # 5
            "simple_type ou array_type",  # 6
            "array ",  # 7
            "[",  # 8
            "LITERAL_INT",  # 9
            "..",  # 10
            "]",  # 11
            "of",  # 12
            "simple_type",  # 13
            "begin",  # 14
            "read",  # 15
            "(",  # 16
            "declaração de variável",  # 17
            ")",  # 18
            "write",  # 19
            ":=",  # 20
            "literal_int, literal_string, ( ou not",  # 21
            "end",  # 22
            "if",  # 23
            "then",  # 24
            "while",  # 25
            "do",  # 26
            ".", # 27
            "Simbolo desconhecido", # 28
        ]

    def erro_mensagem_model(self):
        if self.erro != 0:
            # ["Lexema", "Token", "Linha", "Coluna", "ID", "Valor"]
            print("\nLinha: ", self.linha, " | ", "Coluna: ", self.coluna)
            print(self.elemento)
            print("^")
            print(
                "Erro sintático ",
                self.erro,
                " - É esperado -> " + self.lst_erro[(self.erro - 1)],
            )

            raise SystemExit("Cancelando...")
