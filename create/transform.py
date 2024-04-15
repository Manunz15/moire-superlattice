# Lorenzo Manunza, Università degli Studi di Cagliari, March 2024

import numpy as np
import pandas as pd

class Transform:
    def __init__(self):
        self.pos_keys = ['x', 'y', 'z']
        self.vel_keys = ['vx', 'vy', 'vz']

    def to_array(self, DF: pd.DataFrame, keys: list[str]):
        return DF[keys].to_numpy()
    
    def rotate_vector(self, vect: np.array, angle: float):
        # rotation
        rot = np.array([[np.cos(angle), np.sin(angle), 0],
                [-np.sin(angle), np.cos(angle), 0],
                [0, 0, 1]])
        
        rotated_vect = np.matmul(vect, rot)
                
        return rotated_vect
    
    def permutation(self, DF:pd.DataFrame, perm: dict[int]):
        DF = DF.copy()
        types = self.to_array(DF, keys = ['type'])
        inverted = types.copy()

        for first, second in perm.items():
            inverted[types == first] = second
            inverted[types == second] = first

        DF['type'] = inverted
        
        return DF

    def translation(self, DF: pd.DataFrame, trasl: np.array):
        # translate all atoms
        DF = DF.copy()
        pos = self.to_array(DF, keys = self.pos_keys)
        new_pos = pos + trasl
        DF[self.pos_keys] = new_pos

        return DF
    
    def rotation(self, DF: pd.DataFrame, angle: float, rads: bool = False, center: bool = True):
        # rotate all atoms and velocities
        DF = DF.copy()
        angle = np.deg2rad(angle) if not rads else angle

        # positions
        pos = self.to_array(DF, keys = self.pos_keys)
        new_pos = self.rotate_vector(pos, angle = angle)
        
        center_pos = np.mean(pos, axis = 0)
        new_center_pos = np.mean(new_pos, axis = 0)

        DF[self.pos_keys] = (new_pos + center_pos - new_center_pos) if center else new_pos

        # velocities
        try:
            vel = self.to_array(DF, keys = self.vel_keys)
            DF[self.vel_keys] = self.rotate_vector(vel, angle = angle)
        except:
            pass

        return DF
