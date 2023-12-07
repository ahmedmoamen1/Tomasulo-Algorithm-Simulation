class Instruction:
    def __init__(self, opcode, operands):
        self.opcode = opcode
        self.operands = operands
        self.issue = 0
        self.start_exec = 0
        self.finish_exec = 0
        self.write = 0

class InstructionStatus:
    def __init__(self, inst_number):
        self.inst_number = inst_number
        self.issue_cycle = 0
        self.execute_cycle = 0
        self.writeback_cycle = 0

    def __str__(self):
        return f"Instruction {self.inst_number} Fetched {self.issue_cycle} Executed {self.execute_cycle if self.execute_cycle > 0 else '-'} Write back {self.writeback_cycle if self.writeback_cycle > 0 else '-'}"

class ReservationStation:
    def __init__(self):
        self.busy = False
        self.op = None
        self.vj = None
        self.vk = None
        self.qj = None
        self.qk = None
        self.destination = None
        self.execution_start = None


class TomasuloSimulator:
    def __init__(self):
        self.memory = [0] * 128
        self.registers = [0] * 15
        self.pc = 0
        self.clock_cycles = 0
        self.instructions = []
        self.reservation_stations = [ReservationStation() for _ in range(6)]  # 6 reservation stations
        self.instruction_status_table = []

    def load_program(self, program):
        self.instructions = program

    def get_register_index(self, reg):
        if '(' in reg:
            reg_name = reg.split('(')[1].split(')')[0]
            return int(reg_name[1:])
        else:
            return int(reg[1:])

    def issue(self):
        for i, inst in enumerate(self.instructions):
            if inst.issue == 0:
                self.instructions[i].issue = self.clock_cycles + 1
                return inst
        return None

    def execute(self, inst):
        opcode = inst.opcode
        operands = inst.operands

        if opcode == "LOAD":
            for rs in self.reservation_stations:
                if not rs.busy:
                    rs.busy = True
                    rs.op = "LOAD"
                    rs.vj = self.registers[self.get_register_index(operands[1])]
                    rs.destination = self.get_register_index(operands[0])
                    inst.start_exec = self.clock_cycles + 1
                    rs.execution_start = self.clock_cycles + 1
                    inst.finish_exec = self.clock_cycles + 3  # 2 cycles for LOAD + 1 cycle to write back
                    break
        # Implement logic for MULT, SUB, DIV, ADD in a similar manner...

    def write(self, inst):
        for rs in self.reservation_stations:
            if rs.busy and rs.qj is None and rs.qk is None:
                if rs.op == "LOAD":
                    self.registers[rs.destination] = rs.vj
                # Add similar logic for other instructions (MULT, SUB, DIV, ADD)
                rs.busy = False
                rs.op = None
                rs.vj = None
                rs.vk = None
                rs.qj = None
                rs.qk = None
                rs.destination = None
                inst.finish_exec = self.clock_cycles + 1
                break

    def simulate(self):
        while any([inst.issue == 0 for inst in self.instructions]):
            issued_inst = self.issue()
            if issued_inst:
                self.execute(issued_inst)
                self.write(issued_inst)
                status = InstructionStatus(self.instructions.index(issued_inst) + 1)
                status.issue_cycle = issued_inst.issue
                status.execute_cycle = issued_inst.start_exec
                status.writeback_cycle = issued_inst.finish_exec - 1 if issued_inst.finish_exec > 0 else 0
                self.instruction_status_table.append(status)
            self.clock_cycles += 1

            # Print each clock cycle's instruction status
            print(f"Clock cycle {self.clock_cycles}:")
            for status in self.instruction_status_table:
                print(status)

            # Clear the table for the next cycle
            self.instruction_status_table = []


simulator = TomasuloSimulator()
# Example usage:

simulator = TomasuloSimulator()

program_instructions = [
   Instruction("LOAD", ["R6", "34(R2)"]),
    Instruction("LOAD", ["R2", "45(R3)"]),
    Instruction("MULT", ["R0", "R2", "R3"]),
    Instruction("SUB", ["R8", "R6", "R2"]),
    Instruction("DIV", ["R10", "R0", "R6"]),
    Instruction("ADD", ["R6", "R8", "R2"]),
]

for i, inst in enumerate(program_instructions):
    simulator.instructions.append(inst)

simulator.memory[10] = 15

simulator.simulate()