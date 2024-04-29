def remove_component_value(netlist):
    # Split the input into lines
    lines = netlist.strip().split('\n')
    
    # Prepare to store the modified lines
    modified_lines = []
    
    for line in lines:
        # Check if there is a semicolon indicating the start of a comment
        if ';' in line:
            main_part, comment = line.split(';', 1)
            comment = ';' + comment  # Re-add the semi-colon
        else:
            main_part = line
            comment = ''
        
        # Split the main part of the line into spaces
        parts = main_part.split()
        
        # Remove the fourth element if present
        if len(parts) >= 4:
            # Construct the new line by excluding the fourth part
            new_line = ' '.join(parts[:3])
        else:
            # If there are less than four parts, just keep them as is
            new_line = ' '.join(parts)

        # Append the modified line with the comment, if any
        modified_lines.append(new_line + comment)
    
    # Join all modified lines back into a single string with newlines
    modified_netlist = '\n'.join(modified_lines)
    return modified_netlist

# Example netlist
netlist = """
V 1 0 6; down=1.5
R1 1 2 2; right=1.5
R2 2 0_2 4; down
W 0 0_2; right
"""

# Use the function
new_netlist = remove_component_value(netlist)
print(new_netlist)