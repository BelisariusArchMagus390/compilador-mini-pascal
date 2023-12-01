from pathlib import Path


class WriteStatementsAsmh:
    def __init__(self):
        self.path_file = (
            Path(__file__)
            .parent.joinpath("executable_file")
            .joinpath("executable.asmh")
        )

        self.lines_to_write = []

        self.temp_line_else = []
        self.temp_line_if = []

        self.temp_line_while = []

        self.line_count = 0
        self.line_count_final = 0

        self.line_count_else = 0
        self.line_count_if = 0
        self.line_count_final_if = 0

    def write_in_file(self):
        file_asmh = open(self.path_file, "w")

        for line in self.lines_to_write:
            file_asmh.write(line)

    def write_test_line(self):
        command_lines = " DUMP\n"
        self.lines_to_write.append(command_lines)
        self.line_count += 1

    def write_program_asmh(self):
        command_lines = " INIP\n"
        self.lines_to_write.append(command_lines)
        self.line_count += 1

    def aux_write_decision(self, flag_if, flag_else, flag_while, command_lines, n=0):
        if flag_if == True and flag_else == False and flag_while == False:
            self.temp_line_if.append(command_lines)
            self.line_count_if += 2

        elif flag_if == False and flag_else == True and flag_while == False:
            self.temp_line_else.append(command_lines)
            self.line_count_else += 2

        elif flag_if == False and flag_else == False and flag_while == True:
            if (command_lines in self.temp_line_while) == False:
                self.temp_line_while.append(command_lines)

        else:
            self.lines_to_write.append(command_lines)

    def write_read_asmh(self, memory_position, flag_if, flag_else, flag_while):
        command_lines = f" READ\n STOR {memory_position}\n"
        n = 2

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    def write_asmh(self, text, flag_if, flag_else, flag_while):
        command_lines = f" LDCT {text}\n SHOW\n"
        n = 2

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    # Expressões lógicas
    def write_logic_op_less_than_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
        flag_if,
        flag_else,
        flag_while,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n LETH\n STOR {memory_position_final}\n"
        n = 4

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    def write_logic_op_less_or_equal_than_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
        flag_if,
        flag_else,
        flag_while,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n LEEQ\n STOR {memory_position_final}\n"
        n = 4

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    def write_logic_op_greater_than_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
        flag_if,
        flag_else,
        flag_while,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n GRTH\n STOR {memory_position_final}\n"
        n = 4

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    def write_logic_op_greater_or_equal_than_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
        flag_if,
        flag_else,
        flag_while,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n GREQ\n STOR {memory_position_final}\n"
        n = 4

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    def write_logic_op_equal_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
        flag_if,
        flag_else,
        flag_while,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n EQUA\n STOR {memory_position_final}\n"
        n = 4

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    def write_logic_op_different_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
        flag_if,
        flag_else,
        flag_while,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n DIFF\n STOR {memory_position_final}\n"
        n = 4

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    def write_logic_op_or_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
        flag_if,
        flag_else,
        flag_while,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n _OR_\n STOR {memory_position_final}\n"
        n = 4

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    def write_logic_op_and_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
        flag_if,
        flag_else,
        flag_while,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n AND_\n STOR {memory_position_final}\n"
        n = 4

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    def write_logic_op_not_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
        flag_if,
        flag_else,
        flag_while,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n INVI\n STOR {memory_position_final}\n"
        n = 4

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    # Expressões aritméticas
    def write_arithmetic_op_add_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
        flag_if,
        flag_else,
        flag_while,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n ADD_\n STOR {memory_position_final}\n"
        n = 4

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    def write_arithmetic_op_sub_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
        flag_if,
        flag_else,
        flag_while,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n SUBT\n STOR {memory_position_final}\n"
        n = 4

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    def write_arithmetic_op_div_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
        flag_if,
        flag_else,
        flag_while,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n DIVI\n STOR {memory_position_final}\n"
        n = 4

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    def write_arithmetic_op_mul_asmh(
        self,
        memory_position1,
        memory_position2,
        memory_position_final,
        flag_if,
        flag_else,
        flag_while,
    ):
        command_lines = f" LDVL {memory_position2}\n LDVL {memory_position1}\n MULT\n STOR {memory_position_final}\n"
        n = 4

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    def write_assignment_asmh(
        self, value, memory_position, flag_if, flag_else, flag_while
    ):
        command_lines = f" LDCT {value}\n STOR {memory_position}\n"
        n = 2

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    # Funções para criação do If Else

    # Escreve a condicional do If
    def write_if_conditional_asmh(self, flag_if, flag_else, flag_while):
        command_lines = f" GOIF "

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines)

    # Escreve a label onde ficará o bloco de código do If
    def write_label_if_asmh(self, flag_if, flag_else, flag_while):
        n = 1
        self.line_count += n

        self.line_count_final_if = self.line_count - self.line_count_if + 2

        command_lines = f"L{self.line_count_final_if}\n"

        if self.line_count_else == 0:
            command_lines = command_lines + f" GOTO L{self.line_count + 2}\n"

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

    # Escreve o bloco de código que está contigo no Else
    def write_code_block_else_asmh(self, flag_if, flag_else, flag_while):
        else_code_block = "".join(self.temp_line_else)
        self.temp_line_else.clear()

        n = 1
        self.line_count += n
        self.line_count_final = self.line_count

        command_lines = else_code_block + f" GOTO L{self.line_count_final+1}\n"

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

    # Escreve o bloco de código que está contigo no If
    def write_code_block_if_asmh(self, flag_if, flag_else, flag_while):
        command_lines = f"L{self.line_count_final_if}:"

        if_code_block = "".join(self.temp_line_if)
        self.temp_line_if.clear()

        if self.line_count_else == 0:
            line = self.line_count + 2
        else:
            line = self.line_count_final + 1

        command_lines = command_lines + if_code_block + f"L{line}:"

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines)

    # Funções para criação do while

    # Escreve a label que marcará o inicio do while
    def write_intial_label_while_asmh(self, flag_if, flag_else, flag_while):
        n = 1
        self.line_count += n
        command_lines = f"L{self.line_count}:"
        self.line_count_final = self.line_count

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

    # Escreve a o bloco de código que está dentro do while
    def write_code_block_while_asmh(self, flag_if, flag_else, flag_while):
        command_lines = "".join(self.temp_line_while)
        self.temp_line_while.clear()

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines)

    # Escreve a condicional do while
    def write_while_conditional_asmh(self, flag_if, flag_else, flag_while):
        command_lines = f" GOIF L{self.line_count_final}\n GOTO L{self.line_count+2}\n"
        n = 2

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    # Escreve a label que marcará o fim do while
    def write_final_label_while_asmh(self, flag_if, flag_else, flag_while):
        command_lines = f"L{self.line_count}:"
        self.line_count_final = self.line_count
        n = 1

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines, n)

        self.line_count += n

    # -----------------------------------------------------------------------------------------------------------------

    # Funções ainda a serem feitas

    def write_array_declaration(self, flag_if, flag_else, flag_while):
        command_lines = ""

        self.aux_write_decision(flag_if, flag_else, flag_while, command_lines)

    # -----------------------------------------------------------------------------------------------------------------

    def write_end_program_asmh(self):
        command_lines = " ENDP"
        self.lines_to_write.append(command_lines)
        self.line_count += 1
