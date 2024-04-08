# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

import os
import shutil

class Path:
    def __init__(self, dir: str = '../simulations', path: list[str] = []):
        # initialization
        path.insert(0, dir)
        self.path = self.join(path)
        self.create(self.path)

    def __str__(self) -> str:
        return self.path

    def join(self, path: list[str]) -> str:
        return '/'.join(path)

    def create(self, path: str) -> None:
        if not os.path.isdir(path):
            os.makedirs(path)

    def create_dir(self, dir: str, files: list[str] = []) -> None:
        # create path
        dir_path = self.join([self.path, dir])
        self.create(dir_path)

        # copy files
        for file in files:
            filename = file.split('/')[-1]
            final_path = self.join([dir_path, filename])
            shutil.copy2(file, final_path)

        return dir_path