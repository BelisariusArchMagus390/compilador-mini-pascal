import random as rm
import re

from .error_message_model import ErrorMessage
from .tree import SymbolTable


class Tokenizador:
    def __init__(self):
        self.st = SymbolTable()

        self.codigo = ""
        self.id = r"^[a-zA-Z]([a-zA-Z]|[0-9])*$"
        self.digito_inteiro = r"^[0-9]+$"
        self.string_constante = r"('\S+')"

        self.palavras_reservadas = [
            "while",
            "div",
            "not",
            "if",
            "then",
            "else",
            "of",
            "while",
            "do",
            "begin",
            "end",
            "read",
            "write",
            "var",
            "array",
            "program",
            "true",
            "false",
            "char",
            "integer",
            "boolean",
            "and",
            "or",
            "procedure",
            "function",
        ]

        self.operadores_aritmeticos = ["+", "-", "*"]
        self.operadores_logicos = ["<", ">", "="]
        self.esp_operadores_logicos = ["<>", "<=", ">="]

        self.simbolos_especiais = ["(", ")", "[", "]", "|", ".", ",", ";", ":"]
        self.esp_simbolos_especiais = [":=", ".."]

        self.palavras_chave = (
            self.palavras_reservadas
            + self.operadores_aritmeticos
            + self.operadores_logicos
            + self.simbolos_especiais
        )

        self.esp_simbolos = self.esp_operadores_logicos + self.esp_simbolos_especiais

        self.ids = {}

        self.matriz_tokens = []

        self.erro_elemento = []

    """
    Função que gera o ID do identificador.
    Se houver um identificador idêntico já registrado no vetor lexemas, 
    retornará o seu ID, caso contrário será gerado um ID
    """

    def defini_id(self, lexema):
        if lexema in self.ids:
            return self.ids[lexema]

        new_id = None
        ids_values = self.ids.values()

        while new_id is None or new_id in ids_values:
            new_id = rm.randint(100, 400)

        return new_id

    def tokenizar(self):
        # For que analisará cada char da string codigo
        linha = 1
        coluna = 0
        tipo_token = ""

        erro = False

        # Váriavel que guarda o lexema para a análise
        lexema = ""

        count_aspas = 0
        for i, char in enumerate(self.codigo):
            if char == "'":
                count_aspas += 1

            if count_aspas == 1:
                lexema += char
                continue
            elif count_aspas == 2:
                count_aspas = 0

            if char != " ":
                lexema += char

            if (i + 1) < len(self.codigo):
                next_char = self.codigo[i + 1]
                curr_lex = lexema + next_char

            # Faz a filtragem de todos os lexemas que são separados por espaços
            # vazios e/ou símbolos que são aceitos pela a linguagem
            if (
                next_char == " "
                or next_char in self.palavras_chave
                or lexema in self.palavras_chave
                or curr_lex in self.esp_simbolos
            ):
                if i - 1 >= 0 and (self.codigo[i - 1] + lexema) in self.esp_simbolos:
                    lexema = ""
                    continue

                if lexema != "":
                    coluna += 1

                    if lexema == "\n":
                        coluna = 0
                        linha += 1
                    else:
                        if (
                            re.match(self.string_constante, lexema.replace(" ", ""))
                            != None
                        ):
                            second_item = "LITERAL_STRING"
                            tipo_token = "Literal String"

                        elif lexema in self.palavras_reservadas:
                            if lexema in ["true", "false"]:
                                second_item = "BOOLEAN"
                                tipo_token = "Literal Booleano"
                            else:
                                second_item = lexema
                                tipo_token = "Palavra reservada"

                        elif re.match(self.id, lexema) != None:
                            self.ids[lexema] = self.defini_id(lexema)
                            second_item = "IDENT"
                            tipo_token = "Identificador"

                        elif re.match(self.digito_inteiro, lexema) != None:
                            second_item = "LITERAL_INT"
                            tipo_token = "Literal inteiro"

                        elif curr_lex in self.esp_simbolos:
                            second_item = curr_lex.strip(" ")
                            lexema = curr_lex.strip(" ")
                            tipo_token = "Símbolo especial"
                        elif (
                            curr_lex in self.esp_simbolos
                            or lexema in self.operadores_aritmeticos
                            or lexema in self.operadores_logicos
                            or lexema in self.simbolos_especiais
                        ):
                            second_item = lexema
                            tipo_token = "Símbolo especial"
                        else:
                            erro = True
                            self.erro_elemento.extend([lexema, linha, coluna])
                            break

                        appendable = [lexema, second_item, linha, coluna, tipo_token]
                        self.matriz_tokens.append(appendable)

                    lexema = ""

        if erro == True:
            e = ErrorMessage(
                28, self.erro_elemento[1], self.erro_elemento[2], self.erro_elemento[0]
            )
            e.erro_mensagem_model()

        # Conversão dos valores do dicionário de ids para uma lista
        ids_list = [
            self.ids.get(self.matriz_tokens[i][0])
            for i in range(len(self.matriz_tokens))
        ]

        # Inserção da coluna id
        self.matriz_tokens = [
            self.matriz_tokens[i] + [ids_list[i]]
            for i in range(len(self.matriz_tokens))
        ]

        return self.matriz_tokens

    def set_codigo(self, codigo):
        self.codigo = codigo
        self.codigo = codigo.replace("\n", " \n ")

    def tabela_simbolo(self):
        for lexema, id in self.ids.items():
            self.st.insert(id, lexema)

        return self.st

    def get_st(self):
        return self.st

    def get_matriz_tokens(self):
        return self.matriz_tokens

    def get_table_symbol_values(self):
        return self.st.get_node_matr()
