#!/usr/bin/env python3
import os
import argparse

from parablade.common import *
from parablade.shapeshift import Blades

PrintBannerV2()

# ARGUMENT DEFINITION

parser = argparse.ArgumentParser(description="Merge all the geometries inside a specified folder together to form a new one.")
parser.add_argument(
    "input_folder",
    help="Path to the folder containing the .cfg files to be merged.",
    type=str,
    default=".",
)
parser.add_argument(
    "-m",
    "--mix_equally",
    help="Use this flag to mix all the geometries equally.",
    action="count",
    default=0,
)


args = parser.parse_args()

def recursive_get_files(folder):
    results = []
    for file in os.listdir(folder):
        path = f'{folder}/{file}'
        if os.path.isdir(path):
            results += recursive_get_files(path)
        elif os.path.isfile(path) and path.endswith('parametrized.cfg'):
            results.append(path)
    return results

cfgs = recursive_get_files(args.input_folder)

print(f'List of .cfg files found in {args.input_folder} and subfolders.\nIf a file is missing, make sure it ends with `parametrized.cfg`.')
for i, file in enumerate(cfgs):
    print(f'\t{i}\t\t{file}')

main_index = int(input(
        '\nSelect the index corresponding to the main file.' 
        'The mesh will be built from that:\t'))

main = cfgs[main_index]

main_blade = Blades(main)
# main_blade.plot_variant('base')

if not args.mix_equally:
    print('\n')
    coefs = [float(input(f'\ncoef for main file {main}:\t'))]
    coefs += [float(input(f'coef for {file}:\t')) for file in cfgs[:main_index] + cfgs[main_index+1:]]
else:
    np.ones(len(cfgs))

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
    if coefs[i] != 0:
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
    [coefficient for coefficient in coefs if coefficient != 0]
)

print('\n\nFinal result:')
main_blade.plot_variant(new_name)

filename = input('\nSave blade as (name/n): \t')
if not filename.lower() in ['n', 'no']:
    if filename == '':
        main_blade.write_blade(new_name)
    else:
        main_blade.write_blade(new_name, filename)




    

