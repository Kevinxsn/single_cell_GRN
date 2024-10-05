from pytfmpval import tfmp
import numpy as np

def each_calc(file_name):
    
    with open(f'aertslab_motif_colleciton/v10nr_clust_public/singletons/{file_name}', 'r') as file:
        lines = file.readlines()[1:]
    matrix = np.array([list(map(float, line.split())) for line in lines])
    matrix_transpose = matrix.T
    
    # Round everything into integer
    matrix_transpose = np.round(matrix_transpose)
    matrix_transpose = matrix_transpose.astype(int)
    #print(matrix_transpose)
    if matrix_transpose.shape[0]>9:
        matrix_transpose = matrix_transpose[:9, :]
    
    flattened_list = matrix_transpose.flatten()
    mat_str = " ".join(f"{int(num):2}" for num in flattened_list)
    mat_tuple = (mat_str)

    m = tfmp.read_matrix(mat_tuple)
    new_value = tfmp.pval2score(m, 0.00001)

    # Write as new file
    with open(f'aertslab_motif_colleciton/v10nr_clust_public/singletons/{file_name}', 'r') as file:
        lines = file.readlines()
        
    if lines and lines[0].startswith('>'):
        lines[0] = lines[0].strip() + "\t" + lines[0].strip()[1:] + "\t" + str(new_value) + "\n"
        
    #output_file_path = 'modified_matrix.txt'
    #with open(output_file_path, 'w') as output_file:
    #    output_file.writelines(lines)

    return lines





