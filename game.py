from lcapy import *
from lcapy import Circuit
from lcapy.system import tmpfilename, LatexRunner, PDFConverter
from lcapy import state; state.current_sign_convention = 'passive'
from Extra_Methods.NetlistConverter import remove_component_value

units = {
    'v': 'V',
    'i': 'A',
    'r': 'R',
    'c': 'G'
}


def game_loop(circuit):
    # DC volt divider for beginners
    circuit = Circuit("""
    V 1 0 6; down=1.5
    R1 1 2 2; right=1.5
    R2 2 0_2 4; down
    W 0 0_2; right""")

    empty_circuit = remove_component_value(circuit)

    while True:
        print("\n\nWelcome to the Circuit Solver Game!")
        print("Choose an option:")
        print("1. Solve Circuit")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':

            # Draw circuit 
            empty_circuit.draw()

            # Print Netlist
            print(empty_circuit.netlist())
            component_name = input("Enter the name of the component you want to solve for: ")
            component_property = input("Enter i or v for current or voltage: ")

            # Assuming you have a function to solve for a specific component in Time Domain representation
            solution = request_component_property(circuit, component_name, component_property)
            unit = units[component_property]
            
            latexPrint(solution, unit)
            userAnswer = input("What is the value of the property for the component? ")

            # Check if user answer is correct
            if (solution==int(userAnswer)):
                print("Congratulations! You solved it.")
                latexPrint(solution, unit)
            else:
                print("Sorry, that's not correct. Try again!")
        elif choice == '2':
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

def request_component_property(circuit, componentName, componentProperty):
    try:
        if (componentProperty == 'v'):
            return circuit[componentName].V(t)
        elif (componentProperty == 'i'):
            return circuit[componentName].I(t)
    except KeyError:
        print(f"Error: Component '{componentName}' not found.")
    except AttributeError:
        print(f"Error: Property '{componentProperty}' not found for component '{componentName}'.")
    

def latexPrint(solu, unit):
    # Generate LaTeX and PNG image of mesh equations
    s = solu.latex() + '\\:' + unit

    tex_filename = tmpfilename('.tex')

    # Need amsmath for operatorname
    template = ('\\documentclass[a4paper]{standalone}\n'
                '\\usepackage{amsmath}\n'
                '\\begin{document}\n$%s$\n'
                '\\end{document}\n')
    content = template % s

    open(tex_filename, 'w').write(content)
    pdf_filename = tex_filename.replace('.tex', '.pdf')
    latexrunner = LatexRunner()
    latexrunner.run(tex_filename)

    png_filename = "temp/request.png"
    pdfconverter = PDFConverter()
    pdfconverter.to_png(pdf_filename, png_filename, dpi=300)

    return png_filename

if __name__ == '__main__':
    game_loop(circuit)