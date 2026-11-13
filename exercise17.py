
from file_utils import *
from matrix_utils import *
from string_utils import *

from concurrent.futures import ProcessPoolExecutor


def parse_input(input_string):
    """
    Parsea l'input in due liste:
    - Una per i registri (lista di dizionari chiave-valore)
    - Una per il programma (lista di opcode)

    Args:
        input_string (str): Input formattato contenente registri e programma.

    Returns:
        tuple: (registers, program), dove:
            - registers è un dizionario con chiavi "A", "B", "C" e i rispettivi valori.
            - program è una lista di interi rappresentanti gli opcode.
    """
    registers = {}
    program = []

    lines = input_string.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("Register"):
            # Parse del registro
            parts = line.split(":")
            key = parts[0].split()[1]  # Ottieni "A", "B" o "C"
            value = int(parts[1].strip())
            registers[key] = value
        elif line.startswith("Program"):
            # Parse del programma
            program = list(map(int, line.split(":")[1].strip().split(",")))

    return registers, program


class ThreeBitComputer:
    def __init__(self, registers=None):
        if not registers:
            self.registers = {'A': 0, 'B': 0, 'C': 0}
        else:
            self.registers = registers
        self.instruction_pointer = 0
        self.output = []

    def reset(self):
        self.registers = {'A': 0, 'B': 0, 'C': 0}
        self.instruction_pointer = 0
        self.output = []

    def combo_value(self, operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.registers['A']
        elif operand == 5:
            return self.registers['B']
        elif operand == 6:
            return self.registers['C']
        else:
            raise ValueError("Invalid combo operand")

    def execute_instruction(self, program):
        while self.instruction_pointer < len(program):
            opcode = program[self.instruction_pointer]
            operand = program[self.instruction_pointer + 1]

            if opcode == 0:  # adv
                self.registers['A'] //= 2 ** self.combo_value(operand)
            elif opcode == 1:  # bxl
                self.registers['B'] ^= operand
            elif opcode == 2:  # bst
                self.registers['B'] = self.combo_value(operand) % 8
            elif opcode == 3:  # jnz
                if self.registers['A'] != 0:
                    self.instruction_pointer = operand
                    continue
            elif opcode == 4:  # bxc
                self.registers['B'] ^= self.registers['C']
            elif opcode == 5:  # out
                self.output.append(self.combo_value(operand) % 8)
                #print(f"output: {self.output} : {self.registers["A"]}")
            elif opcode == 6:  # bdv
                self.registers['B'] = self.registers['A'] // (2 ** self.combo_value(operand))
            elif opcode == 7:  # cdv
                self.registers['C'] = self.registers['A'] // (2 ** self.combo_value(operand))
            else:
                raise ValueError(f"Invalid opcode: {opcode}")

            self.instruction_pointer += 2

    def run(self, program):
        self.execute_instruction(program)
        return self.output


def process_value(args):
    idx, program = args
    computer = ThreeBitComputer()
    computer.registers = {'A': idx, 'B': 0, 'C': 0}
    output = computer.run(program)
    return idx if output == program else None


def find_initial_value(program, max_idx=100000):
    with ProcessPoolExecutor() as executor:
        # Passa argomenti come tuple per evitare problemi di serializzazione
        results = executor.map(process_value, ((i, program) for i in range(max_idx-100000, max_idx)))
        for result in results:
            if result is not None:
                return result
    return None


def reconstruct_initial_a(output, base=8):
    current_a = 0  # Partiamo da un valore neutrale
    #13.7148

    # output: [0]: A = 14680
    # output: [0, 3]: A = 1835
    # output: [0, 3, 5]: A = 229
    # output: [0, 3, 5, 4]: A = 28
    # output: [0, 3, 5, 4, 3]: A = 3
    # output: [0, 3, 5, 4, 3, 0]: A = 0
    # Output: [0, 3, 5, 4, 3, 0]
    # A = 117440

    # Risaliamo dall'ultimo valore dell'output al primo
    for value in reversed(output):
        current_a = value + current_a * base
        print(current_a)

    return current_a * base


if __name__ == "__main__":
    file_path = f"./inputs/17/input.txt"
    file_content = read_file_to_string(file_path)

    mode = 1

    if mode == 0:
        registers, program = parse_input(file_content)

        print(registers)
        print(program)

        computer = ThreeBitComputer(registers)
        output = computer.run(program)
        print("Output:", output)
    else:
        _, program = parse_input(file_content)

        # BRUTE FORCE
        result = None
        for i in range(130673376989968, 28265935272522504):
            min_val = i
            max_val = min_val + 100000
            print(f"trying range {min_val} => {max_val}")
            result = find_initial_value(program, max_idx=max_val)

            if result:
                break

        #initial_a = reconstruct_initial_a(program)
        #print(initial_a)
        #print(f"Valore trovato: {int(initial_a)}")

# 28265935272522504   too high
# 130673376989968     too low
# 130673376989968 => 130673376991338 tested