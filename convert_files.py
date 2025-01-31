import json
import sys
from convert import convert_json_files_to_one

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_files.py <destination_all> <json_file1> <json_file2> ...")
        sys.exit(1)
    
    destination_all = sys.argv[1]
    json_files = sys.argv[2:]
    
    convert_json_files_to_one(destination_all, *json_files)