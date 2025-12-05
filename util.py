def get_data(file_path: str, type:str) -> list[str]:
    with open(file_path) as f:
        if type == "lines":
            data = f.read().strip().splitlines()
            
        elif type == "comma":
            data = f.read().strip().split(",")
        else:
            raise ValueError("Ongeldig type opgegeven. Gebruik 'lines' of 'comma'.")
        f.close()
    return data

def parse_range(range_str: str) -> tuple[int, int]:
    start_str, end_str = range_str.split("-")
    return int(start_str), int(end_str)