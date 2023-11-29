from .write_statements_asmh import WriteStatementsAsmh
from .tree import SymbolTable
from .parser_model import Parser
from .error_message_model import ErrorMessage

ERRO_FALTA_MEMORIA = 32


class StatementsAsmh:
    def __init__(self):
        self.was = WriteStatementsAsmh()
        self.tr = SymbolTable()
        self.par = Parser()
        self.memory_position = 0

    def program_asmh(self):
        self.was.write_program_asmh()

    def read_asmh(self, memory_position):
        self.was.write_read_asmh(self, memory_position)

    def write_asmh(self, text):
        self.was.write_asmh(self, text)

    def find_node_id(self, element):
        lexem_matr = self.par.get_matriz_tokens()

        id = None

        for lexem in lexem_matr:
            if element == lexem[0]:
                id = lexem[5]
                break

        return id

    def exist_variable(self, element):
        lexem_matr = self.par.get_matriz_tokens()

        id = None
        memory_position = None
        condition = False

        for lexem in lexem_matr:
            if element == lexem[0]:
                id = lexem[5]
                condition = True
                break

        node = self.tr.search(id)

        memory_position = node.memory_position

        return [condition, memory_position]

    def aux_op(self, element1_value, element2_value):
        memory_position1 = None
        memory_position2 = None

        ifstored1 = False
        ifstored2 = False

        element1 = self.exist_variable(element1_value)
        element2 = self.exist_variable(element2_value)

        if element1[0]:
            ifstored1 = True
            memory_position1 = element1[1]

        if element2[0]:
            ifstored2 = True
            memory_position1 = element2[1]

        return [memory_position1, memory_position2, ifstored1, ifstored2]

    def logic_ops_asmh(
        self,
        op,
        element1_value,
        element2_value,
    ):
        memory_position1, memory_position2, ifstored1, ifstored2 = self.aux_op(
            element1_value, element2_value
        )

        if op == "<":
            self.was.write_logic_op_less_than_asmh(
                ifstored1,
                ifstored2,
                memory_position1,
                memory_position2,
                self.memory_position,
                element1_value,
                element2_value,
            )

        elif op == "<=":
            self.was.write_logic_op_less_or_equal_than_asmh(
                ifstored1,
                ifstored2,
                memory_position1,
                memory_position2,
                self.memory_position,
                element1_value,
                element2_value,
            )

        elif op == ">":
            self.was.write_logic_op_greater_than_asmh(
                ifstored1,
                ifstored2,
                memory_position1,
                memory_position2,
                self.memory_position,
                element1_value,
                element2_value,
            )

        elif op == ">=":
            self.was.write_logic_op_greater_or_equal_than_asmh(
                ifstored1,
                ifstored2,
                memory_position1,
                memory_position2,
                self.memory_position,
                element1_value,
                element2_value,
            )

        elif op == "=":
            self.was.write_logic_op_equal_asmh(
                ifstored1,
                ifstored2,
                memory_position1,
                memory_position2,
                self.memory_position,
                element1_value,
                element2_value,
            )

        elif op == "<>":
            self.was.write_logic_op_different_asmh(
                ifstored1,
                ifstored2,
                memory_position1,
                memory_position2,
                self.memory_position,
                element1_value,
                element2_value,
            )

        elif op == "or":
            self.was.write_logic_op_or_asmh(
                ifstored1,
                ifstored2,
                memory_position1,
                memory_position2,
                self.memory_position,
                element1_value,
                element2_value,
            )

        elif op == "and":
            self.was.write_logic_op_and_asmh(
                ifstored1,
                ifstored2,
                memory_position1,
                memory_position2,
                self.memory_position,
                element1_value,
                element2_value,
            )

        elif op == "not":
            self.was.write_logic_op_not_asmh(
                ifstored1,
                ifstored2,
                memory_position1,
                memory_position2,
                self.memory_position,
                element1_value,
                element2_value,
            )

    def arithmetic_ops_asmh(
        self,
        op,
        element1_value,
        element2_value,
    ):
        memory_position1, memory_position2, ifstored1, ifstored2 = self.aux_op(
            element1_value, element2_value
        )

        if op == "+":
            self.was.write_arithmetic_op_add_asmh(
                ifstored1,
                ifstored2,
                memory_position1,
                memory_position2,
                self.memory_position,
                element1_value,
                element2_value,
            )

        elif op == "-":
            self.was.write_arithmetic_op_sub_asmh(
                ifstored1,
                ifstored2,
                memory_position1,
                memory_position2,
                self.memory_position,
                element1_value,
                element2_value,
            )

        elif op == "div":
            self.was.write_arithmetic_op_div_asmh(
                ifstored1,
                ifstored2,
                memory_position1,
                memory_position2,
                self.memory_position,
                element1_value,
                element2_value,
            )

        elif op == "*":
            self.was.write_arithmetic_op_mul_asmh(
                ifstored1,
                ifstored2,
                memory_position1,
                memory_position2,
                self.memory_position,
                element1_value,
                element2_value,
            )

    def write_assignment_asmh(self, var, value):
        self.was.write_assignment_asmh(value, self.memory_position)

        id = self.find_node_id(var)

        self.tr.edit(id, 7, self.memory_position)
        self.tr.edit(id, 3, value)

        if self.memory_position <= 20:
            self.memory_position += 1
        else:
            e = ErrorMessage(ERRO_FALTA_MEMORIA, None, None, None)

            if self.par.get_iu() == True:
                self.par.set_erro_request(True)
                self.par.set_mensagem_erro(e.get_mensagem_erro())
                raise ValueError()
            else:
                e.erro_mensagem_print()

    def write_array_declaration(self):
        pass

    def write_if_asmh(self):
        pass

    def write_while_asmh(self):
        pass

    def write_end_program_asmh(self):
        self.was.write_end_program_asmh()
