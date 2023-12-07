from flask import Flask, render_template, request
from Tomasulo import TomasuloSimulator, Instruction
app = Flask(__name__)

# Import TomasuloSimulator class and other necessary code

# Define routes and views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    program_instructions = request.form['instructions']
    # Split the entered instructions by newline to get a list of instructions
    program_instructions = program_instructions.split('\n')
    
    # Process program_instructions and convert to the Instruction format
    instructions = []
    for inst in program_instructions:
        parts = inst.split()  # Split instruction into parts
        opcode = parts[0]
        operands = parts[1:] if len(parts) > 1 else []
        instructions.append(Instruction(opcode, operands))  # Assuming Instruction class is imported
        
    # Create a simulator instance and run simulation
    simulator = TomasuloSimulator()
    simulator.load_program(instructions)  # Load the program instructions into the simulator

    # Run the simulation
    simulator.simulate()

    # Get performance metrics from the simulator
    # metrics = simulator.get_performance_metrics()  # Implement this method

    return render_template('result.html', metrics=metrics)

if __name__ == '__main__':
    app.run(debug=True)
