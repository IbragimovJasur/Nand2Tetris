import sys

symbol_table = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}
compBuiltIn = {
    # a = 0
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    # a = 1
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}
destBuiltIn = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}
jumpBuiltIn = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

A_CODE = "0"
C_CODE = "111"


class HackAssembler:

    def __init__(self, file_dir: str, symbol_table: dict) -> None:
        self.file_dir = file_dir
        self.symbol_table = symbol_table
        self.commands = []
        self.machine_code = []
        self.labels = []
        self.memory_address = 16

    def parse(self):
        self.read_commands()
        self.add_labels2symbol_table()
        self.remove_labels_from_commands()
        self.translate_instructions()
        self.write_binary2hack_file()

    def read_commands(self) -> None:
        try:
            with open(self.file_dir) as file:
                lines = file.readlines()
                for line in lines:
                    cleaned_line = line.strip()
                    if not cleaned_line.startswith("//") and not cleaned_line == "":
                        self.commands.append(cleaned_line)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self.file_dir}' not found.")

    def add_labels2symbol_table(self):
        instruct_mem_address = 0    # instruction address in memory
        for command in self.commands:
            if command.startswith("(") and command.endswith(")"):
                label = command[1:-1]
                self.symbol_table[label] = instruct_mem_address    # set label to next instruction address
                self.labels.append(command)
            else:
                instruct_mem_address += 1

    def remove_labels_from_commands(self):
        for label in self.labels:
            self.commands.remove(label)

    def translate_instructions(self):
        for command in self.commands:
            if command.startswith("@"):    # A instruction
                symbol = command[1::]
                self.translate_Ainstruction(symbol)
            else:    # C instruction -> dest=comp;jump
                self.translate_Cinstruction(command)

    def translate_Ainstruction(self, symbol: str):
        if symbol.isdigit():    # @4
            bits15 = self.decimal2binary15bit(int(symbol))
            self.machine_code.append(A_CODE + bits15)
        elif symbol in self.symbol_table.keys():    # @R1
            bits15 = self.decimal2binary15bit(self.symbol_table[symbol])
            self.machine_code.append(A_CODE + bits15)
        else:    # @sum
            self.symbol_table[symbol] = self.memory_address
            self.memory_address += 1
            bits15 = self.decimal2binary15bit(self.symbol_table[symbol])
            self.machine_code.append(A_CODE + bits15)

    def translate_Cinstruction(self, command: str):
        dest, comp, jump = self.split_command2dest_comp_jump(command)
        Cinstruct_bits13 = self.convert_Cinstruction2binary(dest, comp, jump)
        self.machine_code.append(C_CODE + Cinstruct_bits13) 

    def decimal2binary15bit(self, num: int) -> str:
        bits = bin(num)[2:]
        Ainstruct_bits15 = bits.zfill(15)
        return Ainstruct_bits15

    def split_command2dest_comp_jump(self, command: str) -> tuple[str]:
        dest, comp, jump = "", "", ""
        if "=" in command:    # dest
            for idx in range(len(command)):
                if command[idx] == "=":
                    command = command[idx+1::]
                    break
                dest += command[idx]

        # comp & jump
        for idx in range(len(command)):
            if command[idx] == ";":
                jump += command[idx+1::]
                break
            comp += command[idx]
        return dest, comp, jump

    def convert_Cinstruction2binary(self, dest: str, comp: str, jump: str) -> str:
        Cinstruct_bits13 = ""
        Cinstruct_bits13 += compBuiltIn[comp]
        Cinstruct_bits13 += destBuiltIn[dest]
        Cinstruct_bits13 += jumpBuiltIn[jump]
        return Cinstruct_bits13

    def write_binary2hack_file(self):
        new_file_name = self.file_dir[:-4]
        with open(f"{new_file_name}.hack", "w") as file:
            for code in self.machine_code:
                file.write(f"{code}\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 HackAssembler <file_dir>")
    else:
        # Get the file name from the command-line argument
        file_name = sys.argv[1]
        HackAssembler(file_name, symbol_table).parse()
