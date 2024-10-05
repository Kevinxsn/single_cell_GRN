import threshold_calc
import os
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, TimeoutError
import concurrent.futures
import threshold_calc
import multiprocessing

directory_path = 'aertslab_motif_colleciton/v10nr_clust_public/singletons'

all_filenames = []
for root, dirs, files in os.walk(directory_path):
    for filename in files:
        all_filenames.append(filename)

all_filenames.sort()

timeout = 60

skipped_files = []

def run_in_process(filename, result_queue):
    try:
        result = threshold_calc.each_calc(filename)
        result_queue.put(result)
    except Exception as e:
        #result_queue.put(f"Error: {e}")
        result_queue.put(None)

def calculate_with_timeout(filename, timeout):
    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=run_in_process, args=(filename, result_queue))
    process.start()
    process.join(timeout)  # Wait for the process to complete or timeout

    if process.is_alive():
        print(f"Skipped {filename} due to timeout.")
        skipped_files.append(filename)
        process.terminate()  # Terminate the process if it's still running
        process.join()  # Ensure the process has fully terminated
        return None

    if not result_queue.empty():
        return result_queue.get()
    else:
        print(f"An error occurred or no result for {filename}.")
        return None

output_file_path = f'modified_matrix_test_{str(timeout)}s.txt'

# Open the output file once in append mode
with open(output_file_path, 'a') as output_file:
    for i in tqdm(all_filenames):
        each_result = calculate_with_timeout(i, timeout)
        if each_result is not None:
            # Write the result to the file immediately
            output_file.writelines(each_result)
        else:
            print(f"Processing failed or skipped for {i}.")
        #print(i)  # Print the filename being processed
        
        
print(skipped_files)


with open('waiting_time_result.txt', 'a') as result_file:
    result_file.write('\n')
    result_file.write('\n')
    result_file.write('\n' + 'the waiting time that as been set is ' + str(timeout) + 's')
    result_file.write('\n' + 'the skipped files are ' + str(skipped_files))
    result_file.write('\n' + 'the number of skipped files is ' + str(len(skipped_files)))
    