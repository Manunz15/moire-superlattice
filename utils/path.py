# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

import os
from utils.file import copy_file

class Path:
    def __init__(self, initial_path: str = '../simulations', path: list[str] = []) -> None:
        """
        PATH CLASS
        -------------------------------------------------------------------------
        Class for creating a main path with sub-directories, eventually filled 
        with files. 

        Parameters
        ----------
        initial_path : string. Starting point, for our purposes is useful to
            initialized it as '../simulations'.

        path : list of strings. The list of directories to follow from the 
            initial path. 

        For example path = ['graphene', 'test'] will create the folder 
        '../simulation/graphene/test'.

        Properties
        ----------

        Methods
        -------
        join -> None. 
        create -> None.
        copy -> None.
        create_dir -> None.
        """

        # initialization
        path.insert(0, initial_path)
        self.path = self.join(path)
        self.create_dir(self.path)

    def __str__(self) -> str:
        return self.path

    def join(self, path: list[str]) -> str:
        return '/'.join(path)

    def create_dir(self, path: str) -> None:
        if not os.path.isdir(path):
            os.makedirs(path)
        
    def copy(self, filenames: list, in_path: str = None) -> None:
        for filename in filenames:
            if in_path:
                copy_file(filename, in_path)
            else:
                copy_file(filename, self.path)

    def initialize_dir(self, dir: str, filenames: list[str] = []) -> None:
        # create path
        dir_path = self.join([self.path, dir])
        self.create_dir(dir_path)

        # copy files
        self.copy(filenames = filenames, in_path = dir_path)

        return dir_path