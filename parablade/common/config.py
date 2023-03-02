###############################################################################################
#                    ____                 ____  _           _                                 #
#                   |  _ \ __ _ _ __ __ _| __ )| | __ _  __| | ___                            #
#                   | |_) / _` | '__/ _` |  _ \| |/ _` |/ _` |/ _ \                           #
#                   |  __/ (_| | | | (_| | |_) | | (_| | (_| |  __/                           #
#                   |_|   \__,_|_|  \__,_|____/|_|\__,_|\__,_|\___|                           #
#                                                                                             #
###############################################################################################

################################# FILE NAME: PlotBlade.py #####################################
# =============================================================================================#
# author: Roberto, Nitish Anand                                                               |
#    :PhD Candidates,                                                                         |
#    :Power and Propulsion, Energy Technology,                                                |
#    :NTNU, TU Delft,                                                                         |
#    :The Netherlands                                                                         |
#                                                                                             |
#                                                                                             |
# Description:                                                                                |
#                                                                                             |
# =============================================================================================#

import numpy as np
import re
import copy

def write_config_file(OUTFile, IN):
    for key in IN:
        input = str(IN[key])
        output = input.replace("[", "")
        output1 = output.replace("]", "")
        try:
            OUTFile.write("%s=%f\n" % (key, np.real(float(output1))))
        except:
            OUTFile.write("%s=%s\n" % (key, output1))


def su2_config_change(name, dest, par, vals):
    """
    Changes parameter for SU2 configuration file.
    Usage SU2_Config_change(<infile abs dest>,<outfile abs dest>,[<parameter to be changed seperated by ,>],[<values separated by commas])>])
    """
    IN = {}
    infile = open(name, "r")
    for line in infile:
        words = re.split(r"=|%|\n|#", line)
        if not any(words[0] in s for s in ["\n", "%", " ", "#"]):
            words = list(filter(None, words))
            IN[words[0]] = words[1]
    # changing values
    for i in range(len(par)):
        IN[par[i]] = str(vals[i])
    outfile = open(dest, "w")
    for key, value in IN.items():
        if key not in ("DV_VALUE", "DV_PARAM"):
            outfile.write("%s= %s\n" % (key, value))
    outfile.write("%s= %s\n" % ("DV_PARAM", IN["DV_PARAM"]))
    outfile.write("%s= %s\n" % ("DV_VALUE", IN["DV_VALUE"]))
    # outfile.write('DV_KIND= HICKS_HENNE\nDV_PARAM= ( 0.0, 0.05)\nDEFINITION_DV= ( 1 , 1.0 | wall1,wall2  | 0.0 , 0.05  )\nNUMBER_PART= 8\nWRT_CSV_SOL= YES\nGRADIENT_METHOD= DISCRETE_ADJOINT\nDV_MARKER= ( WING )\nDV_VALUE= 0.001')


def write_su2_config_file(ConfigName, TYPE):
    with open(ConfigName, "r") as myfile:
        if TYPE == ("SU2_CFD_AD" or "SU2_DOT_AD"):
            data = myfile.read().replace(
                "MATH_PROBLEM= DIRECT", "MATH_PROBLEM= DISCRETE_ADJOINT"
            )
        elif TYPE == ("SU2_DEF"):
            pass
        else:
            pass


def read_user_input(name, section=None):
    IN = {}
    infile = open(name, "r")
    for line in infile:
        words = re.split("=| |\n|,|[|]", line)
        if not any(words[0] in s for s in ["\n", "%", " ", "#"]):
            words = list(filter(None, words))
            for i in range(0, len(words)):
                try:
                    words[i] = float(words[i])
                except:
                    words[i] = words[i]
            if len(words[1::1]) == 1 and isinstance(words[1], float):
                IN[words[0]] = np.array([words[1]])
            elif len(words[1::1]) == 1 and isinstance(words[1], str):
                IN[words[0]] = words[1]
            else:
                IN[words[0]] = words[1::1]
    infile.close()
    IN["Config_Path"] = name
    if section is None:
        return IN
    else:
        length = len(IN["x_leading"])
        for key, value in IN.items():
            if type(value) == list and len(value) == length:
                IN[key] = np.take(value, section)
        return IN


def write_blade_config_file(name, IN):
    for key in IN:
        input = str(list(IN[key])) if type(IN[key]) == np.ndarray else str(IN[key])
        output = input.replace("[", "")
        output1 = output.replace("]", "")
        name.write("%s=%s\n" % (key, output1))
    name.close()


def config_passer(config):
    """Takes in a path to a config file or directly the parsed dict and returns the parsed dict"""
    if type(config) == str:
        return read_user_input(config)
    elif type(config) == dict:
        return config
    else:
        raise TypeError(
            "Inappropriate argument type: input must be path to cfg or the corresponding dictionary itself"
        )


def numpize(config):
    if type(config["x_leading"]) is not np.ndarray:
        for key in PARAMETER_LIST:
            config[key] = np.array(config[key])
    return config


def scale(IN, scale=1e-3, in_place=False):
    """
    Scales the blade according to the scale factor `scale` by changing the relevant parameters.
    """
    config = IN if in_place else copy.deepcopy(IN)

    config["SCALE_FACTOR"] = scale
    for key in MERIDIONAL_CHANNEL_NAMES[:5]:
        config[key] = np.array(config[key]) * config["SCALE_FACTOR"]

    return config


def descale(IN, in_place=False):
    """
    Scales the blade back to its original scale according to the applied scale factor that is saved in the config file.
    """
    config = IN if in_place else copy.deepcopy(IN)

    for key in MERIDIONAL_CHANNEL_NAMES[:5]:
        config[key] = config[key] / config["SCALE_FACTOR"]
    config["SCALE_FACTOR"] = 1

    return config


def reposition(IN, le, te, in_place=False):
    """
    Sets the position of the leading and trailing edges of the blade based on the coordinates of the leading
    edge `le` and the trailing edge `te`.

    Parameters
    ----------
    IN : dict
        Blade parameter dictionary.
    le : numpy.ndarray
        numpy array of shape (3,) with the 3D coordinates of the leading edge point.
    te : numpy.ndarray
        numpy array of shape (3,) with the 3D coordinates of the trailing edge point.
    
    in_place : bool, optional
        Boolean to set whether the dict should be modified in place or not.
    
    Returns
    -------
    config : dict
        A new modified config dictionary if `in_place` was false. Else, this returns a copy of the modified input
        dictionary.
    """
    config = IN if in_place else copy.deepcopy(IN)

    if config['CASCADE_TYPE'] == 'ANNULAR':
        sign_le = np.where(le[2]<0, -1, 1)
        sign_te = np.where(te[2]<0, -1, 1)

        z1 = sign_le*np.linalg.norm([le[1], le[2]])
        z2 = sign_te*np.linalg.norm([te[1], te[2]])
        y1 = 2*(z1*np.arctan((z1-le[2])/le[1]))
        y2 = 2*(z2*np.arctan((z2-te[2])/te[1]))

        config["stagger"] = np.arctan((y2 - y1) / (te[0] - le[0]))
        config["stagger"] = np.array([np.rad2deg(config["stagger"])])

        config["x_leading"] = np.array([le[0]])
        config["y_leading"] = np.array([y1]) 
        config["z_leading"] = np.array([z1])
        config["x_trailing"] = np.array([te[0]])
        config["z_trailing"] = np.array([z2])
    
    else:
        config["stagger"] = np.arctan((te[1]-le[1]) / (te[0] - le[0]))
        config["stagger"] = np.array([np.rad2deg(config["stagger"])])

        config["x_leading"] = np.array([le[0]])
        config["y_leading"] = np.array([le[1]])
        config["z_leading"] = np.array([le[2]])
        config["x_trailing"] = np.array([te[0]])
        config["z_trailing"] = np.array([te[2]])

    return config


# TODO fix bugs associated with this function.
def fatten(IN, in_place=False):
    """
    \"Fattens\" a blade section in order to help avoiding overlapping of the pressure and suction sides of the
    prescribed and matched geometry on initialisation of the optimization process.

    Parameters
    ----------
    IN : dict
        Blade parameter dictionary to be fattened.
    
    in_place : bool, optional
        Boolean to set whether the dict should be modified in place or not.
    
    Returns
    -------
    config : dict
        The new config dictionary if `in_place` was false. Else, this returns a copy of the modified input dictionary.
    """
    config = IN if in_place else copy.deepcopy(IN)

    for key in ["radius_in", "radius_out"]:
        config[key] = np.array([0.01])
    for key in BLADE_SECTION_CAMBER_THICKNESS[7:]:
        config[key] = np.array(config[key]) * 2

    return config

BLADE_SECTION_CAMBER_THICKNESS = [
    "stagger",
    "theta_in",
    "theta_out",
    "radius_in",
    "radius_out",
    "dist_in",
    "dist_out",
    "thickness_upper_1",
    "thickness_upper_2",
    "thickness_upper_3",
    "thickness_upper_4",
    "thickness_upper_5",
    "thickness_upper_6",
    "thickness_lower_1",
    "thickness_lower_2",
    "thickness_lower_3",
    "thickness_lower_4",
    "thickness_lower_5",
    "thickness_lower_6",
]

MERIDIONAL_CHANNEL_NAMES = [
    "x_leading",
    "y_leading",
    "z_leading",
    "x_trailing",
    "z_trailing",
    "x_hub",
    "z_hub",
    "x_shroud",
    "z_shroud",
]

PARAMETER_LIST = MERIDIONAL_CHANNEL_NAMES[:5]

PARAMETER_LIST.extend(BLADE_SECTION_CAMBER_THICKNESS)


def concatenate_config_files(*configs, verbose=True):
    """Concatenates config files into one that contains all the parameters. The number of values per parameter is not
    required to be the same for all the files."""

    if len(configs) != 1:
        for config in configs[1:]:
            for key in PARAMETER_LIST:
                configs[0][key] = np.hstack((configs[0][key], config[key]))

    if verbose:
        print("\n\n")
        for key in PARAMETER_LIST:
            print(f"\t{key}\t has {configs[0][key].shape[0]} parameters")
        print("\n\n")

    return configs[0]
