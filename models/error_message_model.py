from sys import exit


class ErrorMessage:
    def __init__(self, erro, linha=None, coluna=None, elemento=None):
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
            ".",  # 27
            "Símbolo desconhecido",  # 28
            "uma expressão",  # 29
            "procedure",  # 30
            "function",  # 31
            "Falta de memória",  # 32
        ]

        self.mensagem_erro = []

    def erro_mensagem_model(self):
        if self.elemento != None:
            self.mensagem_erro.extend(
                [
                    f"\nLinha: {self.linha} | Coluna: {self.coluna}",
                    self.elemento,
                    "^",
                    f"Erro sintático {self.erro} - É esperado -> {self.lst_erro[(self.erro - 1)]}",
                    "Cancelando...",
                ]
            )
        else:
            self.mensagem_erro[0] = self.lst_erro[31]

    def erro_mensagem_print(self):
        for linha in self.mensagem_erro:
            print(linha)
        exit(0)

    def get_mensagem_erro(self):
        return self.mensagem_erro
