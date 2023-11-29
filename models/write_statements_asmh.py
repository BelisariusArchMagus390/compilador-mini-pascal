from pathlib import Path


class WriteStatementsAsmh:
    def __init__(self):
        self.path_file = (
            Path(__file__)
            .parent.joinpath("executable_file")
            .joinpath("executable.asmh")
        )

        self.lines_to_write = []

    def write_in_file(self):
        file_asmh = open(self.path_file, "w")

        for line in self.lines_to_write:
            file_asmh.write(line)

    def test_line(self):
        command_lines = "DUMP\n"
        self.lines_to_write.append(command_lines)

    def program_asmh(self):
        command_lines = " INIP\n"
        self.lines_to_write.append(command_lines)

    def read_asmh(self, memory_position):
        command_lines = f" READ\n STOR {memory_position}\n"
        self.lines_to_write.append(command_lines)

    def write_asmh(self, text):
        command_lines = f" LDCT {text}\n SHOW\n"
        self.lines_to_write.append(command_lines)

    # Faz o resgate ou se necessário o armazenamento dos valores para a operação desejada
    def value_in_memory(
        self,
        ifstored1,
        ifstored2,
        memory_position1,
        memory_position2,
        element1_value,
        element2_value,
    ):
        complement = ""

        if ifstored1 == True and ifstored2 == True:
            complement = f" LDVL {memory_position2}\n LDVL {memory_position1}\n"

        elif ifstored1 == True and ifstored2 == False:
            complement = f" LDCL {element2_value}\n STOR {memory_position2}\n LDVL {memory_position2}\n LDVL {memory_position1}\n"

        elif ifstored1 == False and ifstored2 == True:
            complement = f" LDVL {memory_position2}\n LDCL {element1_value}\n STOR {memory_position1}\n LDVL {memory_position1}\n"

        else:
            complement = f" LDCL {element1_value}\n STOR {memory_position1}\n LDCL {element2_value}\n STOR {memory_position2}\n LDVL {memory_position2}\n LDVL {memory_position1}\n"

        return complement

    # Expressões lógicas
    def logic_op_less_than_asmh(
        self,
        ifstored1,
        ifstored2,
        memory_position1,
        memory_position2,
        memory_position_final,
        element1_value,
        element2_value,
    ):
        complement = self.value_in_memory(
            ifstored1,
            ifstored2,
            memory_position1,
            memory_position2,
            element1_value,
            element2_value,
        )

        command_lines = complement + f" LETH\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def logic_op_less_or_equal_than_asmh(
        self,
        ifstored1,
        ifstored2,
        memory_position1,
        memory_position2,
        memory_position_final,
        element1_value,
        element2_value,
    ):
        complement = self.value_in_memory(
            ifstored1,
            ifstored2,
            memory_position1,
            memory_position2,
            element1_value,
            element2_value,
        )

        command_lines = complement + f" LEEQ\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def logic_op_greater_than_asmh(
        self,
        ifstored1,
        ifstored2,
        memory_position1,
        memory_position2,
        memory_position_final,
        element1_value,
        element2_value,
    ):
        complement = self.value_in_memory(
            ifstored1,
            ifstored2,
            memory_position1,
            memory_position2,
            element1_value,
            element2_value,
        )

        command_lines = complement + f" GRTH\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def logic_op_greater_or_equal_than_asmh(
        self,
        ifstored1,
        ifstored2,
        memory_position1,
        memory_position2,
        memory_position_final,
        element1_value,
        element2_value,
    ):
        complement = self.value_in_memory(
            ifstored1,
            ifstored2,
            memory_position1,
            memory_position2,
            element1_value,
            element2_value,
        )

        command_lines = complement + f" GREQ\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def logic_op_equal_asmh(
        self,
        ifstored1,
        ifstored2,
        memory_position1,
        memory_position2,
        memory_position_final,
        element1_value,
        element2_value,
    ):
        complement = self.value_in_memory(
            ifstored1,
            ifstored2,
            memory_position1,
            memory_position2,
            element1_value,
            element2_value,
        )

        command_lines = complement + f" EQUA\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def logic_op_different_asmh(
        self,
        ifstored1,
        ifstored2,
        memory_position1,
        memory_position2,
        memory_position_final,
        element1_value,
        element2_value,
    ):
        complement = self.value_in_memory(
            ifstored1,
            ifstored2,
            memory_position1,
            memory_position2,
            element1_value,
            element2_value,
        )

        command_lines = complement + f" DIFF\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def logic_op_or_asmh(
        self,
        ifstored1,
        ifstored2,
        memory_position1,
        memory_position2,
        memory_position_final,
        element1_value,
        element2_value,
    ):
        complement = self.value_in_memory(
            ifstored1,
            ifstored2,
            memory_position1,
            memory_position2,
            element1_value,
            element2_value,
        )

        command_lines = complement + f" _OR_\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def logic_op_and_asmh(
        self,
        ifstored1,
        ifstored2,
        memory_position1,
        memory_position2,
        memory_position_final,
        element1_value,
        element2_value,
    ):
        complement = self.value_in_memory(
            ifstored1,
            ifstored2,
            memory_position1,
            memory_position2,
            element1_value,
            element2_value,
        )

        command_lines = complement + f" AND_\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def logic_op_not_asmh(
        self,
        ifstored1,
        ifstored2,
        memory_position1,
        memory_position2,
        memory_position_final,
        element1_value,
        element2_value,
    ):
        complement = self.value_in_memory(
            ifstored1,
            ifstored2,
            memory_position1,
            memory_position2,
            element1_value,
            element2_value,
        )

        command_lines = complement + f" INVI\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    # Expressões aritméticas
    def arithmetic_op_add_asmh(
        self,
        ifstored1,
        ifstored2,
        memory_position1,
        memory_position2,
        memory_position_final,
        element1_value,
        element2_value,
    ):
        complement = self.value_in_memory(
            ifstored1,
            ifstored2,
            memory_position1,
            memory_position2,
            element1_value,
            element2_value,
        )

        command_lines = complement + f" ADD_\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def arithmetic_op_sub_asmh(
        self,
        ifstored1,
        ifstored2,
        memory_position1,
        memory_position2,
        memory_position_final,
        element1_value,
        element2_value,
    ):
        complement = self.value_in_memory(
            ifstored1,
            ifstored2,
            memory_position1,
            memory_position2,
            element1_value,
            element2_value,
        )

        command_lines = complement + f" SUBT\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def arithmetic_op_div_asmh(
        self,
        ifstored1,
        ifstored2,
        memory_position1,
        memory_position2,
        memory_position_final,
        element1_value,
        element2_value,
    ):
        complement = self.value_in_memory(
            ifstored1,
            ifstored2,
            memory_position1,
            memory_position2,
            element1_value,
            element2_value,
        )

        command_lines = complement + f" DIVI\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def arithmetic_op_mul_asmh(
        self,
        ifstored1,
        ifstored2,
        memory_position1,
        memory_position2,
        memory_position_final,
        element1_value,
        element2_value,
    ):
        complement = self.value_in_memory(
            ifstored1,
            ifstored2,
            memory_position1,
            memory_position2,
            element1_value,
            element2_value,
        )

        command_lines = complement + f" MULT\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def assignment_asmh(self, value, memory_position, neg_symbol):
        command_lines = f" LDCT {value}\n"

        if neg_symbol == True:
            command_lines = command_lines + " NEGA\n"

        command_lines = command_lines + f" STOR {memory_position}\n"

        self.lines_to_write.append(command_lines)

    def array_declaration(self):
        pass

    def if_asmh(self):
        pass

    def while_asmh(self):
        pass


test = WriteStatementsAsmh()
test.logic_op_less_than_asmh(False, True, 1, 2, 20, 20)
test.write_in_file()
