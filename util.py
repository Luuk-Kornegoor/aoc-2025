import numpy as np

def get_data(file_path: str, type:str) -> list[str]:
    with open(file_path) as f:
        if type == "lines":
            data = f.read().strip().splitlines()
        elif type == "comma":
            data = f.read().strip().split(",")
        elif type == "cephalopod":
            data = f.read().split("\n")
        else:
            raise ValueError("Ongeldig type opgegeven. Gebruik 'lines', 'comma', 'cephalopod'.")
        f.close()
    return data

def parse_range(range_str: str) -> tuple[int, int]:
    start_str, end_str = range_str.split("-")
    return int(start_str), int(end_str)

def dist(p1, p2):
    return np.sqrt(sum((p1[i] - p2[i]) ** 2 for i in range(len(p1))))