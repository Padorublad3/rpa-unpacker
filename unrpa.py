import argparse
from pathlib import Path
from unpack import read_index,unpack_rpa
from time import time
def validate_input_path(path:str) -> Path:
    path_obj = Path(path)
    if path_obj.is_file() and path_obj.suffix.lower() == ".rpa":
        return path_obj
    else:
        raise argparse.ArgumentTypeError("Invalid path")

def validate_output_path(path:str) -> Path:
    path_obj = Path(path)
    if path_obj.exists() and path_obj.is_dir():
        return path_obj
    else:
        raise argparse.ArgumentTypeError("Path must be an existing directory")
        
parser = argparse.ArgumentParser()
parser.add_argument(
    "input_path",
    type=validate_input_path,
    help="Input path"
)
parser.add_argument(
    "-o",
    "--output",
    dest="output_path",
    required=True,
    type=validate_output_path,
    help="Output path"
)

if __name__ == "__main__":
    args = parser.parse_args()
    with open(args.input_path,"rb") as file:
        start_time = time()
        index = read_index(file)
        total = unpack_rpa(file,index,args.output_path)
        end_time = time()
        print("done")
        print(f"Total files extracted: {total}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")