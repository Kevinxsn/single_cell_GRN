# Open the input file in read mode and a new output file to write the changes
with open('motifs.motif', 'r') as infile, open('updated_motifs.motif', 'w') as outfile:
    for line in infile:
        # Check if the line starts with ">"
        if line.startswith('>'):
            # Split the line into parts based on whitespace
            parts = line.split()
            
            # Get the motif name part (the second part)
            motif_name = parts[1]
            
            # Split the motif name by the first underscore to separate the name and organism
            name_parts = motif_name.split('_', 1)
            
            # Capitalize the first letter of the name part and lowercase the rest
            corrected_name = name_parts[0].capitalize() + '_' + name_parts[1]
            
            # Reconstruct the line with the corrected motif name
            new_line = f"{parts[0]}\t{corrected_name}\t{parts[2]}\n"
            
            # Write the corrected line to the output file
            outfile.write(new_line)
        else:
            # If the line doesn't start with ">", just write it as it is
            outfile.write(line)