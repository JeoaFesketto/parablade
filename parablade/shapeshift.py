import copy
import numpy as np

import parablade.common.config as cfg
from parablade.blade_3D import Blade3D

# TODO find a better name for this object

class Blades:
    """
    Object that stores a parametrized blade and all its versions.
    """

    def __init__(self, config_file):

        IN = cfg.ReadUserInput(config_file)
        self.variants = {'base': Blade3D(IN)}
    
    def make_variant(self, variant_name, from_variant='base'):

        variant_object = copy.deepcopy(self.variants[from_variant])
        self.variants[variant_name] = variant_object
    
    def modify(self, variant_name, rotation):

        variant = self.variants[variant_name]
        # le = np.array([
        #     variant.IN["x_leading"],
        #     variant.IN["y_leading"],
        #     variant.IN["z_leading"],
        # ])
        # te = np.array([
        #     variant.IN["x_trailing"],
        #     variant.IN["z_trailing"],
        # ])


        variant.IN["x_trailing"] = np.array([...])
        variant.IN["z_trailing"] = np.array([np.linalg.norm((te[0], te[1]))])

        variant.IN["stagger"] += rotation

        variant.IN["x_trailing"] = np.cos(
            np.rad2deg(variant.IN["stagger"])
            )*variant.IN['CHORD'] + variant.IN['x_leading']      
        