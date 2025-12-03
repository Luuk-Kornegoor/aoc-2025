def get_data(file_path: str, type:str) -> list[str]:
    # Lees input data in
    with open(file_path) as f:
        if type == "lines":
            data = f.read().strip().splitlines()
        elif type == "comma":
            data = f.read().strip().split(",")
        else:
            raise ValueError("Ongeldig type opgegeven. Gebruik 'lines' of 'comma'.")
        f.close()
    return data