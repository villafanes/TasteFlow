#https://www.geeksforgeeks.org/how-to-merge-multiple-json-files-using-python/
import json
import os

def merge_files(file_paths, output_file):
    if os.path.exists(output_file):
        os.remove(output_file)

    merged_data = []
    for path in file_paths:
        with open(path, 'r') as in_file:
            data = json.load(in_file)
            merged_data.extend(data)
    with open(output_file, 'w') as outfile:
        json.dump(merged_data, outfile, indent=2)

