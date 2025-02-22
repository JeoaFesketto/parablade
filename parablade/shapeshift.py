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
        self.config_name = config_file.split("/")[-1].split(".")[0]

        IN = cfg.read_user_input(config_file)
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
    
    def make_variant_from_cfg(self, variant_name, cfg_file):
        IN = cfg.read_user_input(cfg_file)
        self.variants[variant_name] = BladeManipulator(IN)
        
        if self.variants[variant_name].chord.shape[0] != self.variants[variant_name].x_l.shape[0]:
            self.variants[variant_name].chord = (
                self.variants[variant_name].x_t - self.variants[variant_name].x_l
            ) / np.cos(np.deg2rad(self.variants[variant_name].stgr))

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

    def bump_blade(
        self, variant_name, upper_coefficient_matrix=None, lower_coefficient_matrix=None
    ):
        """
        Examples
        --------
        import libraries:
        >>> from scipy.ndimage import gaussian_filter
        >>> import numpy as np
        >>> from parablade.shapeshift import Blades

        create blade object:
        >>> o = Blades('container_DGEN_14/DGEN_14/rotor_DGEN_5_parametrized.cfg')

        make array to be used as filter:
        >>> a = np.zeros((6, o.variants['base'].x_l.shape[0]))
        >>> a[3, 4] = 100
        >>> a = gaussian_filter(a, sigma=2) + 1

        modify the initially created blade. This will make a bump on the upper side of the blade.
        a second matrix or the same can be added for the lower side of the blade:
        >>> o.make_variant('test')
        >>> o.bump_blade('test', a)
        """

        t = copy.deepcopy(self.variants[variant_name])

        if upper_coefficient_matrix is not None:
            t.t_u1 *= upper_coefficient_matrix[0, :]
            t.t_u2 *= upper_coefficient_matrix[1, :]
            t.t_u3 *= upper_coefficient_matrix[2, :]
            t.t_u4 *= upper_coefficient_matrix[3, :]
            t.t_u5 *= upper_coefficient_matrix[4, :]
            t.t_u6 *= upper_coefficient_matrix[5, :]

        if lower_coefficient_matrix is not None:
            t.t_l1 *= lower_coefficient_matrix[0, :]
            t.t_l2 *= lower_coefficient_matrix[1, :]
            t.t_l3 *= lower_coefficient_matrix[2, :]
            t.t_l4 *= lower_coefficient_matrix[3, :]
            t.t_l5 *= lower_coefficient_matrix[4, :]
            t.t_l6 *= lower_coefficient_matrix[5, :]

        self.variants[variant_name] = t

    # def gaussian_coefficient_matrix(self, ):
    #     _coeff = np.zeros((12, self.variants[variant_name].x_l.shape))
    #     _coeff[section, thickness_point] = coefficient

    def get_blade_object(self, variant_name, make_blade=True):
        blade = Blade3D(self.variants[variant_name].IN)
        if make_blade:
            blade.make_blade()
        return blade

    def write_blade(self, variant_name, file_name="default"):
        if file_name == "default":
            file_name = f"{self.config_name}_{variant_name}.cfg"
        cfg.write_blade_config_file(open(file_name, "w"), self.variants[variant_name].IN)

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

    def plot_variant(self, variant_name):
        blade = self.get_blade_object(variant_name)
        plot = BladePlot(blade)
        plot.make_python_plot()
        plt.show()

    def plot_variant_section(self, variant_name, section=0):
        blade = self.get_blade_object(variant_name)
        plot = BladePlot(blade)
        plot.section_plot(section)
        plt.show()

    def flipx_variant(self, variant_name):
        temp = self.variants[variant_name]
        temp.stgr *= -1
        temp.t_i *= -1
        temp.t_o *= -1
        temp.y_l *= -1

        upper_thicknesses = [f"t_u{i+1}" for i in range(6)]
        lower_thicknesses = [f"t_l{i+1}" for i in range(6)]

        for u_t, l_t in zip(upper_thicknesses, lower_thicknesses):
            temp_thickness = getattr(temp, u_t)
            setattr(temp, u_t, getattr(temp, l_t))
            setattr(temp, l_t, temp_thickness)

    def flipz_variant(self, variant_name):
        temp = self.variants[variant_name]
        temp.z_l *= -1
        temp.z_t *= -1

    def delete(self, variant_name):
        del self.variants[variant_name]

    def mix_cfgs(self, variant_name, cfg_file, proportion=50, new_name=None):
        """
        Method to mix two cfg files together to obtain an intermediate one, based on the proportion set. 0 returns the initial file, 100 returns the new one.
        """
        new_IN = BladeManipulator(cfg.read_user_input(cfg_file))
        proportion /= 100

        upper_thicknesses = [f"t_u{i+1}" for i in range(6)]
        lower_thicknesses = [f"t_l{i+1}" for i in range(6)]

        if new_name is None:
            new_name = f"merged_{variant_name}_{cfg_file.split('/')[-1].split('.')[0]}"

        self.make_variant(
            new_name,
            from_variant=variant_name,
        )

        temp = self.variants[new_name]

        for attribute in ["stgr", "t_i", "t_o"] + upper_thicknesses + lower_thicknesses:
            setattr(
                temp,
                attribute,
                (1 - proportion) * getattr(temp, attribute)
                + (proportion) * getattr(new_IN, attribute),
            )

        # returns the name of the new variant for convenience.
        return new_name

    def mix_variants(
        self, variant_name, variants_list, coefficient_list, new_name=None
    ):
        """
        Method to mix N variants together to obtain an intermediate one, based on the proportion set. 0 returns the initial variant, 100 returns the new one.
        """

        upper_thicknesses = [f"t_u{i+1}" for i in range(6)]
        lower_thicknesses = [f"t_l{i+1}" for i in range(6)]

        if new_name is None:
            new_name = f"merged_variants"

        self.make_variant(
            new_name,
            from_variant=variant_name,
        )

        temp = self.variants[new_name]

        coefficient_list = np.array(coefficient_list)
        total = np.sum(coefficient_list)
        coefficient_list = coefficient_list/total

        for attribute in ["stgr", "t_i", "t_o"] + upper_thicknesses + lower_thicknesses:
            values = [
                coefficient_list[i] * getattr(self.variants[variant], attribute)
                for i, variant in enumerate([variant_name] + variants_list)
            ]
            new_value = np.sum(np.array(values), 0)

            setattr(temp, attribute, new_value)

        # returns the name of the new variant for convenience.
        return new_name
