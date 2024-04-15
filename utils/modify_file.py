# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

def modify_file(filename: str, changes: dict[str] = {}):
    # open
    with open(filename, 'r') as f:
        lines = f.readlines()

    # modify
    for index, line in enumerate(lines):
        for old, new in changes.items():
            if old in line:
                line = line.replace(str(old), str(new))
                lines[index] = line

    # save
    with open(filename, 'w') as f:
        f.writelines(lines) 