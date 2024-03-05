from lcapy import *
from lcapy import Circuit
from lcapy import state; state.current_sign_convention = 'passive'

def game_loop():
    # DC volt divider for beginners
    circuit = Circuit("""
    V 1 0 6; down=1.5
    R1 1 2 2; right=1.5
    R2 2 0_2 4; down
    W 0 0_2; right""")

    while True:
        print("\n\nWelcome to the Circuit Solver Game!")
        print("Choose an option:")
        print("1. Solve Circuit")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':

            # Draw circuit 
            circuit.draw()

            # Print Netlist
            print(circuit.netlist())
            component_name = input("Enter the name of the component you want to solve for: ")
            component_property = input("Enter i or v for current or voltage: ")

            # Assuming you have a function to solve for a specific component in Time Domain representation
            solution = request_component_property(circuit, component_name, component_property)
            print("Testing Solution:", solution)
            userAnswer = input("What is the value of the property for the component? ")

            # Check if user answer is correct
            if (solution==int(userAnswer)):
                print("Congratulations! You solved it.")
                print("Solution:", solution)
            else:
                print("Sorry, that's not correct. Try again!")
        elif choice == '2':
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

def request_component_property(circuit, componentName, componentProperty):
    # Testing
    print("Testing")
    # Print the netlist
    print(circuit.netlist())
    # Access component property dynamically
    try:
        if (componentProperty == 'v'):
            return circuit[componentName].V(t)
        elif (componentProperty == 'i'):
            return circuit[componentName].I(t)
    except KeyError:
        print(f"Error: Component '{componentName}' not found.")
    except AttributeError:
        print(f"Error: Property '{componentProperty}' not found for component '{componentName}'.")
    

if __name__ == '__main__':
    game_loop()