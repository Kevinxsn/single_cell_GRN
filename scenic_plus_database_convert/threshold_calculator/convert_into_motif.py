import re
import subprocess
import os

## Normalize into percentage

input_file_name = 'modified_matrix_test_10s.txt'




## Remove the error message


def remove_error_message_with_regex(input_file, output_file):
    # Define the regular expression pattern to match the error message and the content inside single quotes
    pattern = r"Error: could not convert string to float: '.*?'"

    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            # Use regex to remove the error message and the text inside single quotes
            cleaned_line = re.sub(pattern, '', line)
            f_out.write(cleaned_line)

# Use the function to clean your text file
#remove_error_message_with_regex('modified_matrix_test_1s.txt', 'test.txt')

error_message_removed = 'error_message_removed.txt'
remove_error_message_with_regex(input_file_name, error_message_removed)
print('error message removed')


def normalize_motif_file(input_file, output_file):

    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            if line.startswith('>'):
                # Write the naming line as is
                f_out.write(line)
            else:
                # Process matrix lines
                numbers = line.split()
                if numbers:  # Check if line is not empty
                    # Convert to float and normalize
                    numbers = list(map(float, numbers))
                    row_sum = sum(numbers)
                    if row_sum != 0:
                        normalized_numbers = [f"{num / row_sum:.7f}" for num in numbers]
                    else:
                        normalized_numbers = ["0.0000000"] * len(numbers)
                    f_out.write("\t".join(normalized_numbers) + "\n")

# Use the function to process your motif file
#normalize_motif_file('test.txt', 'scenic_plus.motif')

output_file_normalized = 'normalized.txt'
normalize_motif_file(error_message_removed, output_file_normalized)


print('file_normalized')



motif_url = 'https://hocomoco11.autosome.org/final_bundle/hocomoco11/full/HUMAN/mono/HOCOMOCOv11_full_HUMAN_mono_homer_format_0.0001.motif'
result = subprocess.run(['wget', '-q', '-O', 'ho_motifs.motif', motif_url], capture_output=True, text=True)

print(result)

file1_path = "ho_motifs.motif"
file2_path = "normalized.txt"

output_file_path = "combined_motifs.motif"

# Open the first file and read its contents
with open(file1_path, 'r') as file1:
    file1_content = file1.read()

# Open the second file and read its contents
with open(file2_path, 'r') as file2:
    file2_content = file2.read()

# Combine the contents of both files
combined_content = file1_content + "\n" + file2_content  # Add a newline between the two files

# Write the combined content into the output file
with open(output_file_path, 'w') as output_file:
    output_file.write(combined_content)

print(f"Files combined and written to {output_file_path}")



## Modify the name 


with open('combined_motifs.motif', 'r') as infile, open('combined_motifs_name_modified.motif', 'w') as outfile:
    for line in infile:
        # Check if the line starts with '>'
        if line.startswith('>'):
            # Split the line into parts
            parts = line.split()
            # Remove the prefix from the second item
            parts[1] = parts[1].split('__', 1)[-1]
            # Join the parts back together and write to the output file
            outfile.write('\t'.join(parts) + '\n')
        else:
            # Write non '>' lines directly to the output file
            outfile.write(line)
            
            
## find repetitive motif

print('name_modified')


def remove_duplicate_motifs(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    seen_prefixes = set()
    result_lines = []
    skip_entry = False

    for i, line in enumerate(lines):
        if line.startswith('>'):
            # Split the line and get the second element
            elements = line.split()
            if len(elements) > 1:
                second_element = elements[1]
                # Try to extract the prefix before "_"
                prefix = second_element.split('_')[0] if '_' in second_element else second_element
                
                # Check if the prefix has been seen before
                if prefix in seen_prefixes:
                    skip_entry = True
                else:
                    seen_prefixes.add(prefix)
                    skip_entry = False
        
        # If not skipping, add the line to the result
        if not skip_entry:
            result_lines.append(line)

    # Write the filtered entries to the output file
    with open(output_file, 'w') as file:
        file.writelines(result_lines)

# Usage
#input_file = '../data/motifs.motif'
#output_file = '../data/filtered_motifs.motif'
#remove_duplicate_motifs(input_file, output_file)

remove_duplicate_motifs('combined_motifs_name_modified.motif', 'finished_motifs.motif')
print('duplicate motif deleted')
print('convert successful')

print('removing unnecessary files')

file_pathes = ['combined_motifs_name_modified.motif','combined_motifs.motif', 'normalized.txt', 'ho_motifs.motif', 'error_message_removed.txt']

# Remove the file


for file_path in file_pathes:
    try:
        os.remove(file_path)
        print(f"{file_path} has been removed successfully.")
    except FileNotFoundError:
        print(f"{file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")