# Lorenzo Manunza, Università degli Studi di Cagliari, March 2024

import numpy as np
import pandas as pd

class Transform:
    pos_keys = ['x', 'y', 'z']
    vel_keys = ['vx', 'vy', 'vz']

    @staticmethod
    def to_array(df: pd.DataFrame, keys: list[str]) -> np.array:
        return df[keys].to_numpy()
    
    @staticmethod
    def rotate_vector(vect: np.array, angle: float) -> np.array:
        # rotation matrix
        rot = np.array([[np.cos(angle), np.sin(angle), 0],
                [-np.sin(angle), np.cos(angle), 0],
                [0, 0, 1]])
        
        rotated_vect = np.matmul(vect, rot)
                
        return rotated_vect
    
    @staticmethod
    def scale(atoms: pd.DataFrame, factor: float) -> None:
        pos = __class__.to_array(df = atoms, keys = __class__.pos_keys)
        new_pos = pos * factor
        atoms[__class__.pos_keys] = new_pos

    @staticmethod
    def translate(atoms: pd.DataFrame, trasl: list) -> None:
        # translate all atoms
        if type(trasl) == list:
            trasl = np.array(trasl)

        pos = __class__.to_array(df = atoms, keys = __class__.pos_keys)
        new_pos = pos + trasl
        atoms[__class__.pos_keys] = new_pos
    
    @staticmethod
    def rotate(atoms: pd.DataFrame, angle: float, rads: bool = False) -> None:
        # angle to rad
        angle = np.deg2rad(angle) if not rads else angle

        # new positions
        pos = __class__.to_array(df = atoms, keys = __class__.pos_keys)
        new_pos = __class__.rotate_vector(vect = pos, angle = angle)
        atoms[__class__.pos_keys] = new_pos

        # new velocities
        try:
            vel = __class__.to_array(atoms, keys = __class__.vel_keys)
            atoms[__class__.vel_keys] = __class__.rotate_vector(vel, angle = angle)
        except:
            pass

    @staticmethod
    def permutate(atoms: pd.DataFrame, perm: dict[int, int]) -> None:
        types = __class__.to_array(df = atoms, keys = ['type'])
        inverted = types.copy()

        for first, second in perm.items():
            inverted[types == first] = second
            inverted[types == second] = first

        atoms['type'] = inverted