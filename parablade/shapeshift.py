import copy
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

import parablade.common.config as cfg
from parablade.blade_3D import Blade3D
from parablade.blade_plot import BladePlot
from parablade.manipulator import BladeManipulator

# TODO find a better name for this object


class Blades:
    """
    Object that stores a parametrized blade's parameters and all its variants.

    Examples
    --------
    >>> from parablade.shapeshift import Blades

    Creating an instance of the `Blades` object.
    >>> o = Blades('../DECAP/source_param_geometries/DGEN_rotor_8/rotor_DGEN_5_parametrized.cfg')

    Creating a new variant and modifying it. Here `4` correspond to the parameter section index to which to apply the
    modification.
    >>> o.make_variant('scale_10')
    >>> o.modify_section('scale_10', 4, scale=1.10)

    Plotting and writing the blade to a specified file.
    >>> o.plot_blade('scale_10')
    >>> o.write_blade('scale_10', 'test.cfg')
    """

    def __init__(self, config_file):
        self.config_file = config_file

        IN = cfg.ReadUserInput(config_file)
        self.variants = {"base": BladeManipulator(IN)}

        if self.variants["base"].chord.shape[0] != self.variants["base"].x_l.shape[0]:
            self.variants["base"].chord = (
                self.variants["base"].x_t - self.variants["base"].x_l
            ) / np.cos(np.deg2rad(self.variants["base"].stgr))
        
    @property
    def variants_list(self):
        return [key for key, _ in self.variants.items()]

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
        self, variant_name, section, scale=1, rotate=0, smoothing="gaussian"
    ):
        _coeff = np.zeros(self.variants[variant_name].x_l.shape)
        _coeff[section] = 1
        if smoothing == "gaussian":
            _coeff = gaussian_filter(_coeff, sigma=2)
            _coeff = 1 / np.amax(_coeff) * _coeff

        t = copy.deepcopy(self.variants[variant_name])
        t.x_t = (t.x_t - t.x_l) * (1 + (scale - 1) * _coeff) + t.x_l[section]
        t.chord *= 1 + (scale - 1) * _coeff

        t.stgr += rotate * _coeff
        t.t_i += rotate * _coeff
        t.t_o += rotate * _coeff
        t.x_t = np.cos(np.deg2rad(t.stgr)) * t.chord + t.x_l

        self.variants[variant_name] = t

    def get_blade_object(self, variant_name, make_blade=True):
        blade = Blade3D(self.variants[variant_name].IN)
        if make_blade:
            blade.make_blade()
        return blade

    def plot_blade(self, variant_name):
        blade = self.get_blade_object(variant_name)
        plot = BladePlot(blade)
        plot.make_python_plot()
        plt.show()

    def write_blade(self, variant_name, file_name="default"):
        if file_name == "default":
            file_name = f"{self.config_file[-4]}_{variant_name}.cfg"
        cfg.WriteBladeConfigFile(open(file_name, "w"), self.variants[variant_name].IN)

    def batch_modify(
        self,
        section,
        scale=1,
        rotate=0,
        prefix="auto",
        from_variant="base",
    ):
        for s in list(scale):
            for r in list(rotate):
                self.make_variant(
                    f"{prefix}_{section}_{s}_{r}", from_variant=from_variant
                )
                self.modify_section(
                    f"{prefix}_{section}_{s}_{r}",
                    section,
                    scale=s,
                    rotate=r,
                )
