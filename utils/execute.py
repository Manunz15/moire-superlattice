# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

import platform
import subprocess

def execute(**commands: tuple[str, str]) -> None:
    for system, command in commands.items():
        if platform.system() == system:
            subprocess.run(command, shell = True)
            break
    else:
        raise SystemError(f'{platform.system()} is not a supported system.')