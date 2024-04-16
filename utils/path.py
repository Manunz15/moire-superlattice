# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from utils.file import File
import os

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
        
    def copy(self, filenames: list, in_path: str = None):
        for filename in filenames:
            if in_path:
                File().copy(filename, in_path)
            else:
                File().copy(filename, self.path)

    def create_dir(self, dir: str, filenames: list[str] = []) -> None:
        # create path
        dir_path = self.join([self.path, dir])
        self.create(dir_path)

        # copy files
        self.copy(filenames = filenames, in_path = dir_path)

        return dir_path