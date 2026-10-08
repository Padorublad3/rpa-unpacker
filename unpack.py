import pickle
import zlib
from typing import BinaryIO
import io
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module_name, global_name):
        raise pickle.UnpicklingError("Import is prohibited")


def read_index(infile: BinaryIO) -> dict:
        header = infile.read(33)
        if not header.startswith(b"RPA-3.0 "):
            raise ValueError("Unsupported format")
        offset = int(header[8:24], 16)
        key = int(header[25:33], 16)
        infile.seek(offset)
        virtual_file = io.BytesIO(zlib.decompress(infile.read()))
        index = SafeUnpickler(virtual_file).load()

        for filename in index:
                
            index_list = []

            for offset, dlen, start in index[filename]:
                    if start:
                        if not isinstance(start, bytes):
                            start = start.encode("latin-1")
                        index_list.append((start,))

                    index_list.append((offset ^ key, dlen ^ key))

            index[filename] = index_list

        return index
def extract_file(infile:BinaryIO,output_path:Path, file_data:list) -> None:
    with open(output_path,"wb") as out_file:
        for part in file_data:
            if len(part) == 1:
                out_file.write(part[0])
            else:
                offset, length = part
                infile.seek(offset)
                remaining = length
                while remaining > 0:
                    chunk = min(1048576, remaining)
                    data = infile.read(chunk)
                    if not data:
                        break
                    out_file.write(data)
                    remaining-=len(data)



def unpack_rpa(infile: BinaryIO, index : dict, target_path:Path) -> int:
    total = 0
    unique_dirs = {target_path / Path(filename).parent for filename in index}
    for dir in unique_dirs:
        dir.mkdir(parents=True,exist_ok=True)
    for filename, file_data in index.items():
        output_file = target_path / filename
        extract_file(infile,output_file,file_data)
        total+=1
    return total