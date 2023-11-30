from tabulate import tabulate as tb

from .tokenizador import Tokenizador
from .error_message_model import ErrorMessage

from .statements_asmh import StatementsAsmh

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
ERRO_FALTA_PROCEDURE = 30
ERRO_FALTA_FUNCTION = 31
ERRO_FALTA_MEMORIA = 32


class Parser:
    def __init__(self, codigo, iu=True):
        self.codigo = codigo
        self.tk = Tokenizador()
        self.tk.set_codigo(self.codigo)
        self.matriz_tokens = self.tk.tokenizar()

        self.write_asmh = StatementsAsmh()
        self.write_asmh.set_tr(self.tk.get_st())
        self.write_asmh.set_tk(self.tk)

        self.tok = [l[1] for l in self.matriz_tokens]
        self.tok.append("$")

        self.token_atual = self.tok[0]
        self.index = 0

        self.tab_simb = self.tk.tabela_simbolo()

        self.iu = iu

        self.erro_request = False
        self.mensagem_erro = False

        self.index_initial = None
        self.index_final = None
        self.expression_vect = []

    def construct_expression_vect(self):
        lexm = self.index_initial
        lexm_final = self.index_final

        for lexm in range(lexm, lexm_final):
            self.expression_vect.append(self.matriz_tokens[lexm][0])

    def avanca_token(self):
        if self.index < len(self.tok):
            self.index += 1
            self.token_atual = self.tok[self.index]

    def erro_mensagem(self, erro):
        if erro != 0:
            token_info = self.matriz_tokens[self.index - 1]
            e = ErrorMessage(
                erro,
                token_info[2],
                token_info[3],
                token_info[0],
            )
            e.erro_mensagem_model()

            if self.iu == True:
                self.erro_request = True
                self.mensagem_erro = e.get_mensagem_erro()
                raise ValueError()
            else:
                e.erro_mensagem_print()

    def get_erro_request(self):
        return self.erro_request

    def _get_mensagem_erro(self):
        return self.mensagem_erro

    def set_erro_request(self, erro_request):
        self.erro_request = erro_request

    def set_mensagem_erro(self, mensagem_erro):
        self.mensagem_erro = mensagem_erro

    # Função que encontra o token e avança para o próximo
    def encontra_token(self, token_esperado, erro, config):
        # Através do parâmetro config faz com que configure a função para
        # retorna um valor booleano True caso seja configurado como "b", ou não
        # retorna um valor caso seja "d"
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

        self.write_asmh.program_asmh()

        self.block()

        self.encontra_token(["."], ERRO_FALTA_PONTO_FINAL, "d")

        if self.token_atual == "$":
            self.write_asmh.test_line()
            self.write_asmh.end_program_asmh()
            return

    def block(self):
        self.variable_declaration_part()
        self.subroutine_declaration_part()
        self.compound_statement()

    def relational_operator(self):
        operadores = ["=", "<>", "<", "<=", ">=", ">", "and", "or", "not"]
        return self.encontra_token(operadores, 0, "b")

    def adding_operator_or_sign(self):
        return self.encontra_token(["+", "-"], 0, "b")

    def multiplying_operator(self):
        return self.encontra_token(["*", "div"], 0, "b")

    def variable_identifier(self):
        return self.encontra_token(["IDENT"], 0, "b")

    def indexed_variable(self):
        if self.encontra_token(["["], 0, "b"):
            self.expression()
            self.encontra_token(["]"], ERRO_FINAL_COLCHETE, "d")

    def variable(self):
        if self.variable_identifier():
            self.indexed_variable()
        else:
            self.erro_mensagem(ERRO_NAO_FEITA_DECLARACAO_DE_VARIAVEL)

    def aux_var_declr_part(self):
        if self.token_atual == "IDENT":
            self.variable_declaration()
            self.encontra_token([";"], ERRO_PONTO_E_VIRGULA, "d")
            return True

    def factor(self):
        if self.token_atual == "IDENT" and self.tok[self.index + 1] == "(":
            self.function_procedure_statement()
        elif self.token_atual == "IDENT":
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
                self.erro_mensagem(ERRO_FALTA_IDENTIFICADOR)

            c = True
            while c is True:
                if not self.aux_var_declr_part():
                    c = False

    def variable_declaration(self):
        c = True
        while c is True:
            self.encontra_token(["IDENT"], 0, "d")

            if not self.encontra_token([","], 0, "b"):
                c = False

        self.encontra_token([":"], ERRO_FALTA_DOIS_PONTOS_E_UM_IDENTIFICADOR, "d")

        self.type_()

    def type_(self):
        if not (self.simple_type() or self.array_type()):
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
        self.encontra_token(["LITERAL_INT"], ERRO_FALTA_LITERAL_INT, "d")
        self.encontra_token([".."], ERRO_FALTA_DOIS_PONTOS, "d")
        self.encontra_token(["LITERAL_INT"], ERRO_FALTA_LITERAL_INT, "d")

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

            self.encontra_token([";"], 0, "d")

    def subroutine_declaration_part(self):
        if self.token_atual == "procedure":
            self.procedure_declaration()
        elif self.token_atual == "function":
            self.function_declaration()

    def procedure_declaration(self):
        self.encontra_token(["procedure"], ERRO_FALTA_PROCEDURE, "d")
        self.encontra_token(["IDENT"], ERRO_FALTA_IDENTIFICADOR, "d")
        self.formal_parameters()
        self.encontra_token([";"], ERRO_PONTO_E_VIRGULA, "d")
        self.block()

    def function_declaration(self):
        self.encontra_token(["function"], ERRO_FALTA_FUNCTION, "d")
        self.encontra_token(["IDENT"], ERRO_FALTA_IDENTIFICADOR, "d")
        self.formal_parameters()
        self.encontra_token([":"], ERRO_FALTA_DOIS_PONTOS, "d")
        self.type_()
        self.encontra_token([";"], ERRO_PONTO_E_VIRGULA, "d")
        self.block()

    def aux_var_declr_par_sec(self):
        if self.token_atual == "IDENT":
            self.variable_declaration()
            return True

    def formal_parameters(self):
        if self.encontra_token(["("], ERRO_FALTA_COMECO_PARENTESE, "b"):
            if not self.aux_var_declr_par_sec():
                self.erro_mensagem(ERRO_FALTA_IDENTIFICADOR)

            if self.encontra_token([";"], 0, "b"):
                c = True
                while c is True:
                    if not self.aux_var_declr_part():
                        c = False

            self.encontra_token([")"], ERRO_FIM_PARENTESE, "d")

    def parameters(self):
        c = True
        while c is True:
            self.encontra_token(
                ["LITERAL_STRING", "LITERAL_INT", "BOOLEAN", "IDENT"], 0, "d"
            )

            if not self.encontra_token([","], 0, "b"):
                c = False

    # Regras sintáticas alteradas
    # <function_procedure statement> ::= <function_procedure identifier> ( <paramaters> )
    # <parameters> ::= <empty> | <identifier> | <constant> {, <identifier> | <constant> ,}
    # <factor> ::= <function_procedure statement> | <variable> | <constant> | ( <expression> ) | not <factor>

    def function_procedure_statement(self):
        self.encontra_token(["IDENT"], ERRO_FALTA_IDENTIFICADOR, "d")
        self.encontra_token(["("], ERRO_FALTA_COMECO_PARENTESE, "d")
        self.parameters()
        self.encontra_token([")"], ERRO_FIM_PARENTESE, "d")

    def if_statement(self):
        if self.encontra_token(["if"], ERRO_FALTA_IF, "b"):
            self.index_initial = self.index
            self.expression()
            self.index_final = self.index

            self.construct_expression_vect()

            conditional_expression = self.expression_vect
            self.write_asmh.if_conditional_asmh(conditional_expression)

            self.expression_vect.clear()

            if self.encontra_token(["then"], ERRO_FALTA_THEN, "b"):
                self.write_asmh.label_if_asmh()

                self.write_asmh.set_flag_if(True)
                self.statement()
                self.write_asmh.set_flag_if(False)

                if self.encontra_token(["else"], 0, "b"):
                    self.write_asmh.set_flag_else(True)
                    self.statement()
                    self.write_asmh.set_flag_else(False)

                    self.write_asmh.code_block_else_asmh()

                    self.write_asmh.code_block_if_asmh()

    def while_statement(self):
        if self.encontra_token(["while"], ERRO_FALTA_WHILE, "b"):
            self.write_asmh.initial_label_while_asmh()

            self.index_initial = self.index
            self.expression()
            self.index_final = self.index

            self.construct_expression_vect()
            conditional_expression = self.expression_vect

            if self.encontra_token(["do"], ERRO_FALTA_DO, "b"):
                self.write_asmh.set_flag_while(True)
                self.statement()

                self.write_asmh.while_conditional_asmh(conditional_expression)
                self.write_asmh.set_flag_while(False)

                self.write_asmh.code_block_while_asmh()

                self.write_asmh.final_label_while_asmh()

    def statement(self):
        if not (self.simple_statement() or self.structured_statement()):
            self.erro_mensagem(ERRO_FALTA_UMA_EXPRESSAO)

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
            self.write_asmh.read_asmh()
        elif self.token_atual == "write":
            self.write_statement()
            c = True

            text = self.matriz_tokens[self.index - 2][0]
            self.write_asmh.write_asmh(text)
        elif self.token_atual == "IDENT" and self.tok[self.index + 1] == "(":
            self.function_procedure_statement()
            c = True
        elif self.token_atual == "IDENT":
            self.assignment_statement()
            c = True
        return c

    def write_statement(self):
        if self.encontra_token(["write"], ERRO_FALTA_WRITE, "b"):
            if self.encontra_token(["("], ERRO_FALTA_COMECO_PARENTESE, "b"):
                if not (
                    self.encontra_token(["LITERAL_INT"], 0, "b")
                    or self.encontra_token(["LITERAL_STRING"], 0, "b")
                ):
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
        var = self.matriz_tokens[self.index][0]

        self.variable()

        if (
            not self.encontra_token([":="], ERRO_FALTA_SINAL_DE_ATRIBUICAO, "b")
            and self.token_atual == ":"
            or self.token_atual == ","
        ):
            self.erro_mensagem(ERRO_FALTA_VAR)

        self.index_initial = self.index
        self.expression()
        self.index_final = self.index

        self.construct_expression_vect()

        value = self.expression_vect
        if self.write_asmh.assignment_asmh(var, value):
            self.erro_mensagem(ERRO_FALTA_MEMORIA)

        self.expression_vect.clear()

    def mostra_resultado(self):
        print("\nCÓDIGO ANALISADO COM SUCESSO!")

        print("\nTABELA LÉXICA: \n")

        colunas = [
            "Lexema",
            "Token",
            "Linha",
            "Coluna",
            "Tipo Token",
            "ID",
        ]
        print(tb(self.matriz_tokens, headers=colunas, tablefmt="fancy_grid"))

        self.tab_simb.table_show()

    def get_table_symbol_values(self):
        return self.tab_simb.get_node_matr()

    def parse(self):
        self.program()
        if self.iu == False:
            self.mostra_resultado()
