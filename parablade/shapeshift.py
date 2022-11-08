import copy
import numpy as np
from scipy.ndimage import gaussian_filter

import parablade.common.config as cfg
from parablade.manipulator import BladeManipulator

# TODO find a better name for this object


class Blades:
    """
    Object that stores a parametrized blade's parameters and all its variants.
    """

    def __init__(self, config_file):
        IN = cfg.ReadUserInput(config_file)
        self.variants = {"base": BladeManipulator(IN)}
        if self.variants["base"].chord.shape[0] != self.variants["base"].x_l.shape[0]:
            self.variants["base"].chord = (
                self.variants["base"].x_t - self.variants["base"].x_l
            ) / np.cos(np.deg2rad(self.variants["base"].stgr))

    def make_variant(self, variant_name, from_variant="base"):
        self.variants[variant_name] = copy.deepcopy(self.variants[from_variant])

    def modify_blade(self, variant_name, scale=1, rotate=0):
        t = copy.deepcopy(self.variants[variant_name])
        t.x_t = (t.x_t - t.x_l) * scale + t.x_l
        t.chord *= scale

        t.stgr += rotate
        t.t_i += rotate
        t.t_o += rotate
        t.x_t = np.cos(np.deg2rad(t.stgr)) * t.chord + t.x_l

        self.variants[variant_name] = t

    def modify_section(
        self, variant_name, section, scale=1, rotate=0
    ):
        pedoncule = np.zeros(self.variants[variant_name].x_l.shape)
        pedoncule[section] = 1
        _coeff = gaussian_filter(pedoncule, sigma=2)
        print(_coeff)
        _coeff = 1/np.amax(_coeff)*_coeff
        print(_coeff)

        t = copy.deepcopy(self.variants[variant_name])
        t.x_t = (t.x_t - t.x_l) * (1 + (scale - 1) * _coeff) + t.x_l[
            section
        ]
        t.chord *= (1 + (scale - 1) * _coeff)

        t.stgr += rotate * _coeff
        t.t_i += rotate * _coeff
        t.t_o += rotate * _coeff
        t.x_t = (
            np.cos(np.deg2rad(t.stgr)) * t.chord + t.x_l
        )

        self.variants[variant_name] = t
