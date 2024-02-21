from lcapy import Circuit

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
            #component_name = component_name.strip()
            #component_property = component_property.strip()
            # Assuming you have a function to solve for a specific component
            solution = request_component_property(circuit, component_name, component_property)
            userAnswer = input("What is the value of the property for the component? ")
            # Extract the numerical value from the ConstantTimeDomainVoltage object
            solution_value = solution.dc.magnitude
            if (solution_value-userAnswer == 0):
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
        component = circuit[componentName]
        property_value = getattr(component, componentProperty)
        property_value.pprint()
        return property_value
    except KeyError:
        print(f"Error: Component '{componentName}' not found.")
    except AttributeError:
        print(f"Error: Property '{componentProperty}' not found for component '{componentName}'.")

if __name__ == '__main__':
    game_loop()