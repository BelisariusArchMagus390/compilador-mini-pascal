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

    def write_test_line(self):
        command_lines = "DUMP\n"
        self.lines_to_write.append(command_lines)

    def write_program_asmh(self):
        command_lines = " INIP\n"
        self.lines_to_write.append(command_lines)

    def write_read_asmh(self, memory_position):
        command_lines = f" READ\n STOR {memory_position}\n"
        self.lines_to_write.append(command_lines)

    def write_asmh(self, text):
        command_lines = f" LDCT {text}\n SHOW\n"
        self.lines_to_write.append(command_lines)

    # Expressões lógicas
    def write_logic_op_less_than_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n LETH\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def write_logic_op_less_or_equal_than_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n LEEQ\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def write_logic_op_greater_than_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n GRTH\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def write_logic_op_greater_or_equal_than_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n GREQ\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def write_logic_op_equal_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n EQUA\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def write_logic_op_different_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n DIFF\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def write_logic_op_or_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n _OR_\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def write_logic_op_and_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n AND_\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def write_logic_op_not_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n INVI\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    # Expressões aritméticas
    def write_arithmetic_op_add_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n ADD_\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def write_arithmetic_op_sub_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n SUBT\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def write_arithmetic_op_div_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n DIVI\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def write_arithmetic_op_mul_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n MULT\n STOR {memory_position_final}\n"
        self.lines_to_write.append(command_lines)

    def write_assignment_asmh(self, value, memory_position):
        command_lines = f" LDCT {value}\n STOR {memory_position}\n"

        self.lines_to_write.append(command_lines)

    def write_array_declaration(self):
        pass

    def write_if_asmh(self):
        pass

    def write_while_asmh(self):
        pass

    def write_end_program_asmh(self):
        command_lines = " ENDP"
        self.lines_to_write.append(command_lines)


test = WriteStatementsAsmh()
test.write_logic_op_less_than_asmh(False, True, 1, 2, 20, 20)
test.write_in_file()
