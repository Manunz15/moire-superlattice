# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

import shutil

class File:
    def copy(self, filename: str, path: str) -> None:
        """
        COPY FILES
        -------------------------------------------------------------------------
        Function for copying files from one directory to another. 

        Parameters
        ----------
        filename : string. The name of the file to be copied.

        path : string. The destination path where the file will be copied. 
        """

        shutil.copy2(filename, path)

    def replace(self, filename: str, replacements: dict[str] = {}) -> None:
        """
        REPLACE IN FILES
        -------------------------------------------------------------------------
        Function for replacing strings in a file with others. 

        Parameters
        ----------
        filename : string. The name of the file where the strings will be 
            replaced.
        
        replacements : dictionary of strings. The keys are the strings to be 
            replaced, and the values are the strings that will replace the keys.
            Each key must have only one corresponding value. 

            For example, with replacements = {'hello': 'hola', '15': '42'} 
            every occurrence of 'hello' in the file will be replaced with 'hola', 
            and every occurrence '15' will be replaced with '42'.
        """

        # open
        with open(filename, 'r') as f:
            lines = f.readlines()

        # replace
        for index, line in enumerate(lines):
            for old, new in replacements.items():
                if old in line:
                    line = line.replace(str(old), str(new))
                    lines[index] = line

        # save
        with open(filename, 'w') as f:
            f.writelines(lines) 