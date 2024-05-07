# Lorenzo Manunza, Università degli Studi di Cagliari, March 2024

import numpy as np
import pandas as pd

class Transform:
    def __init__(self) -> None:
        self.pos_keys = ['x', 'y', 'z']
        self.vel_keys = ['vx', 'vy', 'vz']

    def to_array(self, df: pd.DataFrame, keys: list[str]) -> np.array:
        return df[keys].to_numpy()
    
    def rotate_vector(self, vect: np.array, angle: float) -> np.array:
        # rotation matrix
        rot = np.array([[np.cos(angle), np.sin(angle), 0],
                [-np.sin(angle), np.cos(angle), 0],
                [0, 0, 1]])
        
        rotated_vect = np.matmul(vect, rot)
                
        return rotated_vect
    
    def scale(self, atoms: pd.DataFrame, factor: float) -> None:
        pos = self.to_array(df = atoms, keys = self.pos_keys)
        new_pos = pos * factor
        atoms[self.pos_keys] = new_pos

    def translate(self, atoms: pd.DataFrame, trasl: list) -> None:
        # translate all atoms
        if type(trasl) == list:
            trasl = np.array(trasl)

        pos = self.to_array(df = atoms, keys = self.pos_keys)
        new_pos = pos + trasl
        atoms[self.pos_keys] = new_pos
    
    def rotate(self, atoms: pd.DataFrame, angle: float, rads: bool = False, center: bool = True) -> None:
        # rotate all atoms and velocities
        angle = np.deg2rad(angle) if not rads else angle

        # positions
        pos = self.to_array(df = atoms, keys = self.pos_keys)
        new_pos = self.rotate_vector(vect = pos, angle = angle)
        atoms[self.pos_keys] = new_pos
        
        # centering
        center_pos = np.mean(pos, axis = 0)
        new_center_pos = np.mean(new_pos, axis = 0)

        # atoms[self.pos_keys] = (new_pos + center_pos - new_center_pos) if center else new_pos

        # velocities
        try:
            vel = self.to_array(atoms, keys = self.vel_keys)
            atoms[self.vel_keys] = self.rotate_vector(vel, angle = angle)
        except:
            pass

    def permutate(self, atoms: pd.DataFrame, perm: dict[int, int]) -> None:
        types = self.to_array(df = atoms, keys = ['type'])
        inverted = types.copy()

        for first, second in perm.items():
            inverted[types == first] = second
            inverted[types == second] = first

        atoms['type'] = inverted