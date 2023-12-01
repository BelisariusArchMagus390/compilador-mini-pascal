from .write_statements_asmh import WriteStatementsAsmh
from .tree import SymbolTable
from .tokenizador import Tokenizador


class StatementsAsmh:
    def __init__(self, ui=False):
        self.was = WriteStatementsAsmh()
        self.tr = SymbolTable()
        self.tk = Tokenizador()
        self.memory_position = 0
        self.ui = ui
        self.memory_vector_temp = []

        self.flag_if = False
        self.flag_else = False
        self.flag_while = False

    def set_tr(self, tr):
        self.tr = tr

    def set_tk(self, tk):
        self.tk = tk

    def set_flag_if(self, condition):
        self.flag_if = condition

    def set_flag_else(self, condition):
        self.flag_else = condition

    def set_flag_while(self, condition):
        self.flag_while = condition

    def get_flag_while(self):
        return self.flag_while

    def test_line(self):
        self.was.write_test_line()

    def program_asmh(self):
        self.was.write_program_asmh()

    def read_asmh(self):
        self.was.write_read_asmh(
            self.memory_position, self.flag_if, self.flag_else, self.flag_while
        )

    def write_asmh(self, text):
        self.was.write_asmh(text, self.flag_if, self.flag_else, self.flag_while)

    def find_node_id(self, element):
        lexem_matr = self.tk.get_matriz_tokens()

        id = None

        for line in range(len(lexem_matr)):
            if element == lexem_matr[line][0]:
                id = lexem_matr[line][5]
                break

        return id

    def exist_variable(self, element):
        lexem_matr = self.tk.get_matriz_tokens()

        id = None
        memory_position = None
        condition = False

        for lexem in lexem_matr:
            if element == lexem[0] and lexem[1] == "IDENT":
                id = lexem[5]
                condition = True
                break

        if condition == True:
            node = self.tr.search(id)
            memory_position = node.data[7]

        return [condition, memory_position]

    def aux_op_ifstored(self, element1_value, element2_value):
        ifstored1 = False
        ifstored2 = False

        element1 = self.exist_variable(element1_value)
        element2 = self.exist_variable(element2_value)

        if element1[0]:
            ifstored1 = True

        if element2[0]:
            ifstored2 = True

        return [ifstored1, ifstored2]

    def aux_op_memory_position(self, element1_value, element2_value):
        memory_position1 = None
        memory_position2 = None

        element1 = self.exist_variable(element1_value)
        element2 = self.exist_variable(element2_value)

        if element1[1] == None:
            memory_position1 = self.memory_vector_temp[0]
        else:
            memory_position1 = element1[1]

        if element2[1] == None:
            memory_position2 = self.memory_vector_temp[len(self.memory_vector_temp) - 1]
        else:
            memory_position2 = element2[1]

        return [memory_position1, memory_position2]

    def aux_assingment_literal(self, value):
        self.was.write_assignment_asmh(
            value, self.memory_position, self.flag_if, self.flag_else, self.flag_while
        )

        self.memory_vector_temp.append(self.memory_position)

        if self.memory_position <= 20:
            self.memory_position += 1
            return False
        else:
            return True

    def ifstored(
        self,
        element1_value,
        element2_value,
    ):
        ifstored1, ifstored2 = self.aux_op_ifstored(element1_value, element2_value)

        if ifstored1 == False and ifstored2 == True:
            if self.aux_assingment_literal(element1_value):
                return True
        elif ifstored1 == True and ifstored2 == False:
            if self.aux_assingment_literal(element2_value):
                return True
        elif ifstored1 == False and ifstored2 == False:
            if self.aux_assingment_literal(element1_value):
                return True
            if self.aux_assingment_literal(element2_value):
                return True

    def logic_ops_asmh(
        self,
        op,
        element1_value,
        element2_value,
    ):
        if self.ifstored(element1_value, element2_value):
            return True

        memory_position1, memory_position2 = self.aux_op_memory_position(
            element1_value, element2_value
        )

        if op == "<":
            self.was.write_logic_op_less_than_asmh(
                memory_position1,
                memory_position2,
                self.memory_position,
                self.flag_if,
                self.flag_else,
                self.flag_while,
            )

        elif op == "<=":
            self.was.write_logic_op_less_or_equal_than_asmh(
                memory_position1,
                memory_position2,
                self.memory_position,
                self.flag_if,
                self.flag_else,
                self.flag_while,
            )

        elif op == ">":
            self.was.write_logic_op_greater_than_asmh(
                memory_position1,
                memory_position2,
                self.memory_position,
                self.flag_if,
                self.flag_else,
                self.flag_while,
            )

        elif op == ">=":
            self.was.write_logic_op_greater_or_equal_than_asmh(
                memory_position1,
                memory_position2,
                self.memory_position,
                self.flag_if,
                self.flag_else,
                self.flag_while,
            )

        elif op == "=":
            self.was.write_logic_op_equal_asmh(
                memory_position1,
                memory_position2,
                self.memory_position,
                self.flag_if,
                self.flag_else,
                self.flag_while,
            )

        elif op == "<>":
            self.was.write_logic_op_different_asmh(
                memory_position1,
                memory_position2,
                self.memory_position,
                self.flag_if,
                self.flag_else,
                self.flag_while,
            )

        elif op == "or":
            self.was.write_logic_op_or_asmh(
                memory_position1,
                memory_position2,
                self.memory_position,
                self.flag_if,
                self.flag_else,
                self.flag_while,
            )

        elif op == "and":
            self.was.write_logic_op_and_asmh(
                memory_position1,
                memory_position2,
                self.memory_position,
                self.flag_if,
                self.flag_else,
                self.flag_while,
            )

        elif op == "not":
            self.was.write_logic_op_not_asmh(
                memory_position1,
                memory_position2,
                self.memory_position,
                self.flag_if,
                self.flag_else,
                self.flag_while,
            )

        return False

    def arithmetic_ops_asmh(
        self,
        op,
        element1_value,
        element2_value,
    ):
        if self.ifstored(element1_value, element2_value):
            return True

        memory_position1, memory_position2 = self.aux_op_memory_position(
            element1_value, element2_value
        )

        if op == "+":
            self.was.write_arithmetic_op_add_asmh(
                memory_position1,
                memory_position2,
                self.memory_position,
                self.flag_if,
                self.flag_else,
                self.flag_while,
            )

        elif op == "-":
            self.was.write_arithmetic_op_sub_asmh(
                memory_position1,
                memory_position2,
                self.memory_position,
                self.flag_if,
                self.flag_else,
                self.flag_while,
            )

        elif op == "div":
            self.was.write_arithmetic_op_div_asmh(
                memory_position1,
                memory_position2,
                self.memory_position,
                self.flag_if,
                self.flag_else,
                self.flag_while,
            )

        elif op == "*":
            self.was.write_arithmetic_op_mul_asmh(
                memory_position1,
                memory_position2,
                self.memory_position,
                self.flag_if,
                self.flag_else,
                self.flag_while,
            )

        return False

    def expression_value(self, expression):
        arithmetic_op = ["+", "-", "div", "*"]
        logical_op = ["=", "<>", "<", "<=", ">=", ">", "and", "or", "not"]

        if "(" in expression and ")" in expression:
            expression.remove("(")
            expression.remove(")")

        exit = False

        while exit is False:
            val1 = expression[0]
            op = expression[1]
            val2 = expression[2]

            if op in arithmetic_op:
                self.arithmetic_ops_asmh(op, val1, val2)
            elif op in logical_op:
                self.logic_ops_asmh(op, val1, val2)

            expression.remove(val1)
            expression.remove(op)
            expression.remove(val2)

            if len(expression) < 3:
                exit = True

    def assignment_asmh(self, var, value):
        vl = None
        id = self.find_node_id(var)

        self.tr.edit(id, 7, self.memory_position)

        if len(value) > 1:
            self.expression_value(value)
            vl = "expression"
        else:
            vl = value[0]
            self.was.write_assignment_asmh(
                vl,
                self.memory_position,
                self.flag_if,
                self.flag_else,
                self.flag_while,
            )

        self.tr.edit(id, 3, vl)

        self.memory_vector_temp.clear()

        if self.memory_position <= 20:
            self.memory_position += 1
            return False
        else:
            return True

    # Funções para o If Else
    def if_conditional_asmh(self, conditional_expression):
        self.expression_value(conditional_expression)

        self.was.write_if_conditional_asmh(
            self.flag_if,
            self.flag_else,
            self.flag_while,
        )

    def label_if_asmh(self):
        self.was.write_label_if_asmh(
            self.flag_if,
            self.flag_else,
            self.flag_while,
        )

    def code_block_else_asmh(self):
        self.was.write_code_block_else_asmh(
            self.flag_if,
            self.flag_else,
            self.flag_while,
        )

    def code_block_if_asmh(self):
        self.was.write_code_block_if_asmh(
            self.flag_if,
            self.flag_else,
            self.flag_while,
        )

    # Funções para o While
    def initial_label_while_asmh(self):
        self.was.write_intial_label_while_asmh(
            self.flag_if, self.flag_else, self.flag_while
        )

    def code_block_while_asmh(self):
        self.was.write_code_block_while_asmh(
            self.flag_if,
            self.flag_else,
            self.flag_while,
        )

    def while_conditional_asmh(self, conditional_expression):
        self.expression_value(conditional_expression)
        self.was.write_while_conditional_asmh(
            self.flag_if, self.flag_else, self.flag_while
        )

    def final_label_while_asmh(self):
        self.was.write_final_label_while_asmh(
            self.flag_if, self.flag_else, self.flag_while
        )

    def array_declaration(self):
        pass

    def end_program_asmh(self):
        self.was.write_end_program_asmh()

        self.was.write_in_file()
