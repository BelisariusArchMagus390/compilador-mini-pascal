from tabulate import tabulate as tb

from .tokenizador import Tokenizador
from .error_message_model import ErrorMessage

ERRO_FALTA_PROGRAM = 1
ERRO_FALTA_IDENTIFICADOR = 2
ERRO_PONTO_E_VIRGULA = 3
ERRO_FALTA_VAR = 4
ERRO_FALTA_DOIS_PONTOS_E_UM_IDENTIFICADOR = 5
ERRO_NAO_E_SIMPLE_TYPE_OU_ARRAY_TYPE = 6
ERRO_FALTA_ARRAY = 7
ERRO_COMECO_COLCHETE = 8
ERRO_FALTA_LITERAL_INT = 9
ERRO_FALTA_DOIS_PONTOS = 10
ERRO_FINAL_COLCHETE = 11
ERRO_FALTA_OF = 12
ERRO_FALTA_SIMPLE_TYPE = 13
ERRO_FALTA_BEGIN = 14
ERRO_FALTA_READ = 15
ERRO_FALTA_COMECO_PARENTESE = 16
ERRO_NAO_FEITA_DECLARACAO_DE_VARIAVEL = 17
ERRO_FIM_PARENTESE = 18
ERRO_FALTA_WRITE = 19
ERRO_FALTA_SINAL_DE_ATRIBUICAO = 20
ERRO_FALTA_LITERAL_INT_OU_LITERAL_STRING_OU_COMECO_PARENTESE_OU_NOT = 21
ERRO_FALTA_END = 22
ERRO_FALTA_IF = 23
ERRO_FALTA_THEN = 24
ERRO_FALTA_WHILE = 25
ERRO_FALTA_DO = 26
ERRO_FALTA_PONTO_FINAL = 27
ERRO_FALTA_UMA_EXPRESSAO = 29


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
            lexema = i[0]
            if lexema in self.dic_carac:
                valor = self.dic_carac[lexema]
                tipo = valor[0]
                tam_matriz = valor[1]

                if len(i) > 5 and i[5] != None:
                    carac = [tipo, i[5], tam_matriz]
                    i.pop()
                else:
                    carac = [tipo, None, tam_matriz]
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
                self.dic_carac[self.matriz_tokens[i][0]] = [tipo, None]

        elif c == "array":
            tipo = "array " + self.matriz_tokens[self.index - 1][0]
            for i in self.lst_index_tipo:
                lexema = self.matriz_tokens[i][0]
                if lexema in self.dic_carac:
                    self.dic_carac[lexema][0] = tipo
                else:
                    self.dic_carac[lexema] = [tipo, None]

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
        while c is True:
            linha_matriz = self.matriz_tokens[count]

            if linha_matriz[1] == ";":
                c = False
            else:
                valor += linha_matriz[0]
                count += 1
        count_regulado = self.index - 2
        lexema = self.matriz_tokens[count_regulado]
        if not lexema[1] == "IDENT":
            count_regulado = self.index - 5

        lexema.append(valor)

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
        self.encontra_token(["program"], ERRO_FALTA_PROGRAM, "d")

        self.encontra_token(["IDENT"], ERRO_FALTA_IDENTIFICADOR, "d")

        self.encontra_token([";"], ERRO_PONTO_E_VIRGULA, "d")

        # block
        self.variable_declaration_part()
        self.statement_part()

        self.encontra_token(["."], ERRO_FALTA_PONTO_FINAL, "d")

        if self.token_atual == "$":
            return

    def relational_operator(self):
        operadores = ["=", "<>", "<", "<=", ">=", ">", "or", "and"]
        return self.encontra_token(operadores, 0, "b")

    def adding_operator_or_sign(self):
        return self.encontra_token(["+", "-"], 0, "b")

    def multiplying_operator(self):
        return self.encontra_token(["*", "div"], 0, "b")

    def entire_variable_or_array(self):
        if self.variable_identifier():
            self.avanca_token()
            return True

    def variable_identifier(self):
        return (
            self.token_atual == "IDENT"
            or self.token_atual == "LITERAL_INT"
            or self.token_atual == "LITERAL_STRING"
        )

    def array_variable(self):
        if self.entire_variable_or_array():
            return True

    def indexed_variable(self):
        if self.encontra_token(["["], 0, "b"):
            self.expression()
            self.encontra_token(["]"], ERRO_FINAL_COLCHETE, "d")
            return True

    def variable(self):
        if self.entire_variable_or_array():
            self.indexed_variable()
        else:
            self.erro_mensagem(ERRO_NAO_FEITA_DECLARACAO_DE_VARIAVEL)

    def aux_var_declr_part(self):
        if self.token_atual == "IDENT":
            self.variable_declaration()
            self.encontra_token([";"], ERRO_PONTO_E_VIRGULA, "d")
            return True

    def factor(self):
        if self.token_atual == "IDENT":
            self.variable()
        else:
            if not self.encontra_token(
                ["LITERAL_STRING", "LITERAL_INT", "BOOLEAN"], 0, "b"
            ):
                if self.encontra_token(["("], 0, "b"):
                    self.expression()
                    self.encontra_token([")"], ERRO_FIM_PARENTESE, "d")
                elif self.encontra_token(
                    ["not"],
                    ERRO_FALTA_LITERAL_INT_OU_LITERAL_STRING_OU_COMECO_PARENTESE_OU_NOT,
                    "b",
                ):
                    self.factor()

    def term(self):
        self.factor()

        c = True
        while c is True:
            if self.multiplying_operator():
                self.factor()
            else:
                c = False

    def simple_expression(self):
        self.adding_operator_or_sign()
        self.term()

        c = True
        while c is True:
            if self.adding_operator_or_sign():
                self.term()
            else:
                c = False

    def expression(self):
        self.simple_expression()

        if self.relational_operator():
            self.expression()

    def variable_declaration_part(self):
        if self.encontra_token(["var"], 0, "b"):
            if not self.aux_var_declr_part():
                self.erro_mensagem(2)

            c = True
            while c is True:
                if not self.aux_var_declr_part():
                    c = False

    def variable_declaration(self):
        c = True
        while c is True:
            self.lst_index_tipo.append(self.index)
            self.encontra_token(["IDENT"], 0, "d")

            if not self.encontra_token([","], 0, "b"):
                c = False

        self.encontra_token([":"], ERRO_FALTA_DOIS_PONTOS_E_UM_IDENTIFICADOR, "d")

        self.type_()

    def type_(self):
        if self.simple_type():
            self.atribui_tipo("simple")
        elif self.array_type():
            self.atribui_tipo("array")
        else:
            self.erro_mensagem(ERRO_NAO_E_SIMPLE_TYPE_OU_ARRAY_TYPE)

    def simple_type(self):
        return self.encontra_token(["char", "integer", "boolean"], 0, "b")

    def array_type(self):
        self.encontra_token(["array"], ERRO_FALTA_ARRAY, "d")

        if self.encontra_token(["["], ERRO_COMECO_COLCHETE, "b"):
            self.index_range()

        self.encontra_token(["]"], ERRO_FINAL_COLCHETE, "d")

        self.encontra_token(["of"], ERRO_FALTA_OF, "d")

        if not self.simple_type():
            self.erro_mensagem(ERRO_FALTA_SIMPLE_TYPE)

        return True

    def index_range(self):
        self.atribui_tam_matriz()

        self.encontra_token(["LITERAL_INT"], ERRO_FALTA_LITERAL_INT, "d")
        self.encontra_token([".."], ERRO_FALTA_DOIS_PONTOS, "d")
        self.encontra_token(["LITERAL_INT"], ERRO_FALTA_LITERAL_INT, "d")

    def statement_part(self):
        self.compound_statement()

    def compound_statement(self):
        if self.encontra_token(["begin"], ERRO_FALTA_BEGIN, "b"):
            self.statement()
            c = True
            while c is True:
                if self.encontra_token([";"], 0, "b"):
                    self.statement()
                else:
                    c = False
            self.encontra_token(["end"], ERRO_FALTA_END, "d")

    def if_statement(self):
        if self.encontra_token(["if"], ERRO_FALTA_IF, "b"):
            self.expression()
            if self.encontra_token(["then"], ERRO_FALTA_THEN, "b"):
                self.statement()
                if self.encontra_token(["else"], 0, "b"):
                    self.statement()

    def while_statement(self):
        if self.encontra_token(["while"], ERRO_FALTA_WHILE, "b"):
            self.expression()
            if self.encontra_token(["do"], ERRO_FALTA_DO, "b"):
                self.statement()

    def statement(self):
        lol = self.simple_statement()
        if lol:
            return
        lal = self.structured_statement()
        if lal:
            return
        # self.erro_mensagem(ERRO_FALTA_UMA_EXPRESSAO)

    """
    def statement(self):
        if not (self.simple_statement() or self.structured_statement()):
            print(self.token_atual)
            self.erro_mensagem(ERRO_FALTA_UMA_EXPRESSAO)
    """

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
        if self.encontra_token(["write"], ERRO_FALTA_WRITE, "b"):
            if self.encontra_token(["("], ERRO_FALTA_COMECO_PARENTESE, "b"):
                self.variable()
                c = True
                while c is True:
                    if self.encontra_token([","], 0, "b"):
                        self.variable()
                    else:
                        c = False
                self.encontra_token([")"], ERRO_FIM_PARENTESE, "d")

    def read_statement(self):
        if self.encontra_token(["read"], ERRO_FALTA_READ, "b"):
            if self.encontra_token(["("], ERRO_FALTA_COMECO_PARENTESE, "b"):
                self.variable()
                c = True
                while c is True:
                    if self.encontra_token([","], 0, "b"):
                        self.variable()
                    else:
                        c = False
                self.encontra_token([")"], ERRO_FIM_PARENTESE, "d")

    def assignment_statement(self):
        self.variable()

        if (
            not self.encontra_token([":="], ERRO_FALTA_SINAL_DE_ATRIBUICAO, "b")
            and self.token_atual == ":"
            or self.token_atual == ","
        ):
            self.erro_mensagem(ERRO_FALTA_VAR)

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
