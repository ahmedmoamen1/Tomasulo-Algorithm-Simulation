class Instruction:
    def __init__(self, opcode, operands):
        self.opcode = opcode
        self.operands = operands
        self.issue = 0
        self.start_exec = 0
        self.finish_exec = 0
        self.write = 0


class ReservationStation:
    def __init__(self):
        self.busy = False
        self.op = None
        self.vj = None
        self.vk = None
        self.qj = None
        self.qk = None
        self.destination = None


class TomasuloSimulator:
    def __init__(self):
        self.memory = [0] * 128
        self.registers = [0] * 8
        self.pc = 0
        self.clock_cycles = 0
        self.instructions = []
        self.reservation_stations = [ReservationStation() for _ in range(6)]  # 6 reservation stations

    def load_program(self, program):
        # Load program instructions
        self.instructions = program

    def issue(self):
        # Find an instruction to issue
        for i, inst in enumerate(self.instructions):
            if inst.issue == 0:
                self.instructions[i].issue = self.clock_cycles + 1
                return inst

        return None

    def execute(self, inst):
        opcode = inst.opcode
        operands = inst.operands

        if opcode == "LOAD":
            # Execute load operation
            pass  # Implement load execution logic
        elif opcode == "STORE":
            # Execute store operation
            pass  # Implement store execution logic
        elif opcode == "BNE":
            # Execute branch if not equal operation
            pass  # Implement BNE execution logic
        elif opcode == "CALL":
            # Execute call operation
            pass  # Implement CALL execution logic
        elif opcode == "RET":
            # Execute return operation
            pass  # Implement RET execution logic
        elif opcode == "ADD":
            # Execute add operation
            pass  # Implement ADD execution logic
        elif opcode == "ADDI":
            # Execute add immediate operation
            pass  # Implement ADDI execution logic
        elif opcode == "NAND":
            # Execute NAND operation
            pass  # Implement NAND execution logic
        elif opcode == "DIV":
            # Execute divide operation
            pass  # Implement DIV execution logic

    def write(self, inst):
        opcode = inst.opcode
        operands = inst.operands

        if opcode in ["LOAD", "ADD", "ADDI", "NAND", "DIV"]:
            # Write result to register
            destination_register = operands[0]
            result = self.reservation_stations[self.find_station_by_destination(destination_register)].vj
            self.registers[int(destination_register[1])] = result
            # Update reservation station and register status
            station_idx = self.find_station_by_destination(destination_register)
            self.reservation_stations[station_idx].busy = False
            self.reservation_stations[station_idx].op = None
            self.reservation_stations[station_idx].vj = None
            self.reservation_stations[station_idx].vk = None
            self.reservation_stations[station_idx].qj = None
            self.reservation_stations[station_idx].qk = None
            self.reservation_stations[station_idx].destination = None
        elif opcode == "STORE":
            # No need to perform write for STORE operation as the store was done in execute method
            pass
        elif opcode == "BNE":
            # No write needed for branch instructions
            pass
        elif opcode in ["CALL", "RET"]:
            # No write needed for call and return instructions
            pass

    def simulate(self):
            while any([inst.issue == 0 for inst in self.instructions]):
                # Issue instructions
                issued_inst = self.issue()
                if issued_inst:
                    self.execute(issued_inst)
                    self.write(issued_inst)

                # Increment clock cycle after each cycle
                self.clock_cycles += 1

            # Calculate performance metrics
            total_instructions = len(self.instructions)
            execution_time = self.clock_cycles
            ipc = total_instructions / execution_time if execution_time > 0 else 0


# Example usage:

# Create simulator instance
simulator = TomasuloSimulator()

# Load assembly program instructions
program_instructions = [
    Instruction("LOAD", ["R1", "10(R2)"]),
    Instruction("ADDI", ["R3", "R1", "5"]),
    # Add more instructions as needed
]

for i, inst in enumerate(program_instructions):
    simulator.instructions.append(inst)

# Load data into memory
# Example: Load value 15 into memory address 10
simulator.memory[10] = 15

# Run simulation
simulator.simulate()
