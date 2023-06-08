from tabulate import tabulate as tb

from .tokenizador import Tokenizador
from .error_message_model import ErrorMessage


class Parser:
    def __init__(self, codigo):
        self.codigo = codigo
        self.tk = Tokenizador(self.codigo)
        self.matriz_tokens = self.tk.tokenizar()

        self.tok = [l[1] for l in self.matriz_tokens]
        self.tok.append("$")

        self.lst_index_tipo = []
        self.dic_carac = {}

        self.token_atual = self.tok[0]
        self.index = 0

    # Funções auxiliares
    def complementa(self):
        for i in self.matriz_tokens:
            if i[0] in self.dic_carac:
                if len(i) > 5 and i[5] != None:
                    carac = [self.dic_carac[i[0]][0], i[5], self.dic_carac[i[0]][1]]
                    i.pop()
                    i.extend(carac)
                else:
                    carac = [self.dic_carac[i[0]][0], None, self.dic_carac[i[0]][1]]
                    i.extend(carac)
            elif len(i) > 5 and i[5] != None:
                carac = [None, i[5], None]
                i.pop()
                i.extend(carac)
            elif len(i) == 5:
                i.extend([None, None, None])

    # atribui através de um dicionário
    def atribui_tipo(self, c):
        if c == "simple":
            tipo = self.matriz_tokens[self.index - 1][0]
            for i in self.lst_index_tipo:
                # self.matriz_tokens[i].extend([tipo, None, None])

                self.dic_carac[self.matriz_tokens[i][0]] = [tipo, None]

        elif c == "array":
            tipo = "array " + self.matriz_tokens[self.index - 1][0]
            for i in self.lst_index_tipo:
                # self.matriz_tokens[i].insert(5, tipo)

                if self.matriz_tokens[i][0] in self.dic_carac:
                    self.dic_carac[self.matriz_tokens[i][0]][0] = tipo
                else:
                    self.dic_carac[self.matriz_tokens[i][0]] = [tipo, None]

        self.lst_index_tipo.clear()

    def atribui_tam_matriz(self):
        tamanho_matriz = (
            self.matriz_tokens[self.index][0]
            + self.matriz_tokens[self.index + 1][0]
            + self.matriz_tokens[self.index + 2][0]
        )

        self.dic_carac[self.matriz_tokens[self.index - 4][0]] = [None, tamanho_matriz]

    def atribui_valor(self):
        c = True
        count = self.index
        valor = ""
        while c == True:
            if self.matriz_tokens[count][1] == ";":
                c = False
            else:
                valor += self.matriz_tokens[count][0]
                count += 1
        count_regulado = self.index - 2
        if self.matriz_tokens[count_regulado][1] == "IDENT":
            self.matriz_tokens[count_regulado].append(valor)
        else:
            count_regulado = self.index - 5
            self.matriz_tokens[count_regulado].append(valor)

    def avanca_token(self):
        if self.index < len(self.tok):
            self.index += 1
            self.token_atual = self.tok[self.index]

    def erro_mensagem(self, erro):
        token_info = self.matriz_tokens[self.index - 1]
        e = ErrorMessage(
            erro,
            token_info[2],
            token_info[3],
            token_info[0],
        )
        e.erro_mensagem_model()

    # d = Default, b = Boolean
    def encontra_token(self, token_esperado, erro, config):
        if self.token_atual in token_esperado:
            if config == "d":
                self.avanca_token()
            elif config == "b":
                self.avanca_token()
                return True
        else:
            self.erro_mensagem(erro)

    def program(self):
        self.encontra_token(["program"], 1, "d")

        self.encontra_token(["IDENT"], 2, "d")

        self.encontra_token([";"], 3, "d")

        self.block()

        self.encontra_token(["."], 27, "d")

        if self.token_atual == "$":
            return

    def block(self):
        self.variable_declaration_part()

        self.statement_part()

    def relational_operator(self):
        operadores = ["=", "<>", "<", "<=", ">=", ">", "or", "and"]
        if self.encontra_token(operadores, 0, "b"):
            return True

    def adding_operator_or_sign(self):
        if self.encontra_token(["+", "-"], 0, "b"):
            return True

    def multiplying_operator(self):
        if self.encontra_token(["*", "div"], 0, "b"):
            return True

    def entire_variable_or_array(self):
        if self.variable_identifier():
            self.avanca_token()
            return True

    def variable_identifier(self):
        if (
            self.token_atual == "IDENT"
            or self.token_atual == "LITERAL_INT"
            or self.token_atual == "LITERAL_STRING"
        ):
            return True

    def array_variable(self):
        if self.entire_variable_or_array():
            return True

    def indexed_variable(self):
        if self.encontra_token(["["], 0, "b"):
            self.expression()
            self.encontra_token(["]"], 10, "d")
            return True

    def variable(self):
        if self.entire_variable_or_array():
            if self.indexed_variable():
                return
            else:
                return
        else:
            self.erro_mensagem(17)

    def aux_var_declr_part(self):
        if self.token_atual == "IDENT":
            self.variable_declaration()
            self.encontra_token([";"], 3, "d")
            return True

    def factor(self):
        if self.token_atual == "IDENT":
            self.variable()
        elif self.encontra_token(["LITERAL_STRING", "LITERAL_INT", "BOOLEAN"], 0, "b"):
            return
        elif self.encontra_token(["("], 0, "b"):
            self.expression()
            self.encontra_token([")"], 18, "d")
        elif self.encontra_token(["not"], 21, "b"):
            self.factor()

    def term(self):
        self.factor()

        c = True
        while c == True:
            if self.multiplying_operator():
                self.factor()
            else:
                c = False

    def simple_expression(self):
        self.adding_operator_or_sign()
        self.term()

        c = True
        while c == True:
            if self.adding_operator_or_sign():
                self.term()
            else:
                c = False

    def expression(self):
        self.simple_expression()

        if self.relational_operator():
            self.expression()

    def variable_declaration_part(self):
        if not self.encontra_token(["var"], 0, "b"):
            return

        if not self.aux_var_declr_part():
            self.erro_mensagem(2)

        c = True
        while c == True:
            if not self.aux_var_declr_part():
                c = False

    def variable_declaration(self):
        c = True
        while c == True:
            self.lst_index_tipo.append(self.index)
            self.encontra_token(["IDENT"], 0, "d")

            if not self.encontra_token([","], 0, "b"):
                c = False

        self.encontra_token([":"], 5, "d")

        self.type_()

    def type_(self):
        if self.simple_type():
            self.atribui_tipo("simple")
        elif self.array_type():
            self.atribui_tipo("array")
        else:
            self.erro_mensagem(6)

    def simple_type(self):
        if self.encontra_token(["char", "integer", "boolean"], 0, "b"):
            return True

    def array_type(self):
        self.encontra_token(["array"], 7, "d")

        if self.encontra_token(["["], 8, "b"):
            self.index_range()

        self.encontra_token(["]"], 11, "d")

        self.encontra_token(["of"], 12, "d")

        if not self.simple_type():
            self.erro_mensagem(13)

        return True

    def index_range(self):
        self.atribui_tam_matriz()

        self.encontra_token(["LITERAL_INT"], 9, "d")
        self.encontra_token([".."], 10, "d")
        self.encontra_token(["LITERAL_INT"], 9, "d")

    def statement_part(self):
        self.compound_statement()

    def compound_statement(self):
        if self.encontra_token(["begin"], 14, "b"):
            self.statement()
            c = True
            while c == True:
                if self.encontra_token([";"], 0, "b"):
                    self.statement()
                else:
                    c = False
            self.encontra_token(["end"], 22, "d")

    def if_statement(self):
        if self.encontra_token(["if"], 23, "b"):
            self.expression()
            if self.encontra_token(["then"], 24, "b"):
                self.statement()
                if self.encontra_token(["else"], 0, "b"):
                    self.statement()

    def while_statement(self):
        if self.encontra_token(["while"], 25, "b"):
            self.expression()
            if self.encontra_token(["do"], 26, "b"):
                self.statement()

    def statement(self):
        if self.simple_statement():
            return
        elif self.structured_statement():
            return

    def structured_statement(self):
        c = False
        if self.token_atual == "begin":
            self.compound_statement()
            c = True
        elif self.token_atual == "if":
            self.if_statement()
            c = True
        elif self.token_atual == "while":
            self.while_statement()
            c = True

        return c

    def simple_statement(self):
        c = False
        if self.token_atual == "read":
            self.read_statement()
            c = True
        elif self.token_atual == "write":
            self.write_statement()
            c = True
        elif self.token_atual == "IDENT":
            self.assignment_statement()
            c = True
        else:
            return c

    def write_statement(self):
        if self.encontra_token(["write"], 19, "b"):
            if self.encontra_token(["("], 16, "b"):
                self.variable()
                c = True
                while c == True:
                    if self.encontra_token([","], 0, "b"):
                        self.variable()
                    else:
                        c = False
                self.encontra_token([")"], 18, "d")

    def read_statement(self):
        if self.encontra_token(["read"], 15, "b"):
            if self.encontra_token(["("], 16, "b"):
                self.variable()
                c = True
                while c == True:
                    if self.encontra_token([","], 0, "b"):
                        self.variable()
                    else:
                        c = False
                self.encontra_token([")"], 18, "d")

    def assignment_statement(self):
        self.variable()

        if (
            not self.encontra_token([":="], 20, "b")
            and self.token_atual == ":"
            or self.token_atual == ","
        ):
            self.erro_mensagem(4)

        self.atribui_valor()

        self.expression()

    def mostra_resultado(self):
        print("\nCÓDIGO ANALISADO COM SUCESSO!")

        print("\nTABELA DE SÍMBOLOS: \n")

        colunas = [
            "Lexema",
            "Token",
            "Linha",
            "Coluna",
            "ID",
            "Tipo",
            "Valor",
            "Tamanho da Matriz",
        ]
        print(tb(self.matriz_tokens, headers=colunas, tablefmt="fancy_grid"))

    def parse(self):
        self.program()
        self.complementa()
        self.mostra_resultado()
