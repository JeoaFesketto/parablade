import os
import argparse

from parablade.common import *
from parablade.shapeshift import Blades

def recursive_get_files(folder):
    results = []
    for file in os.listdir(folder):
        path = f'{folder}/{file}'
        if os.path.isdir(path):
            results += recursive_get_files(path)
        elif os.path.isfile(path) and path.endswith('parametrized.cfg'):
            results.append(path)
    return results

def build_blade(geomvector, input_folder='/scratch/daep/j.fesquet/source_files/param_geometries/base_rotors',
                main_index=0):
    cfgs = recursive_get_files(input_folder)

    main = cfgs[main_index]

    main_blade = Blades(main)

    new_cfgs = []

    def _check_radial(variant):
        return (main_blade.variants[variant].z_l[-1]>main_blade.variants[variant].z_l[0])

    def _check_rotation(variant):
        return (main_blade.variants[variant].stgr[-1]>main_blade.variants[variant].stgr[0])

    # finding orientation
    radial_positive = _check_radial('base')
    # the compressor convention is positive rotation direction
    rotation_positive = _check_rotation('base')

    for i, file in enumerate([main]+cfgs[:main_index] + cfgs[main_index+1:]):
        if geomvector[i] != 0:
            main_blade.make_variant_from_cfg(file, file)
            new_cfgs.append(file)
            # main_blade.plot_variant(file)
            if _check_radial(file) is not radial_positive:
                main_blade.flipz_variant(file)
            if _check_rotation(file) is not rotation_positive:
                main_blade.flipx_variant(file)
            # main_blade.plot_variant(file)


    new_name = main_blade.mix_variants(
        main,
        new_cfgs[1:],
        [coefficient for coefficient in geomvector if coefficient != 0]
    )

    print('\n\nFinal result:')
    main_blade.plot_variant(new_name)