###############################################################################################
#                    ____                 ____  _           _                                 #
#                   |  _ \ __ _ _ __ __ _| __ )| | __ _  __| | ___                            #
#                   | |_) / _` | '__/ _` |  _ \| |/ _` |/ _` |/ _ \                           #
#                   |  __/ (_| | | | (_| | |_) | | (_| | (_| |  __/                           #
#                   |_|   \__,_|_|  \__,_|____/|_|\__,_|\__,_|\___|                           #
#                                                                                             #
###############################################################################################

################################# FILE NAME: PlotBlade.py #####################################
#=============================================================================================#
# author: Roberto, Nitish Anand                                                               |
#    :PhD Candidates,                                                                         |
#    :Power and Propulsion, Energy Technology,                                                |
#    :NTNU, TU Delft,                                                                         |
#    :The Netherlands                                                                         |
#                                                                                             |
#                                                                                             |
# Description:                                                                                |
#                                                                                             |
#=============================================================================================#

from contextlib import redirect_stderr
import enum
import numpy as np
import re
import pdb
import copy
import cmath

# TODO change name convention, functions should be all lower case with underscores for readibility if necesary
# TODO no abbreviations!
def WriteConfigFile(OUTFile,IN):
    #pdb.set_trace()
    for key in IN:
        input = str(IN[key])
        output = input.replace('[','')
        output1 = output.replace(']', '')
        try:
            OUTFile.write("%s=%f\n"%(key,np.real(float(output1))))
        except:
            #pdb.set_trace()
            OUTFile.write("%s=%s\n" % (key, output1))

def SU2_Config_change(name,dest,par,vals):
    '''
    Changes parameter for SU2 configuration file.
    Usage SU2_Config_change(<infile abs dest>,<outfile abs dest>,[<parameter to be changed seperated by ,>],[<values separated by commas])>])
    '''
    IN = {}
    infile = open(name,'r')
    for line in infile:
      words = re.split(r'=|%|\n|#',line)
      if not any(words[0] in s for s in ['\n','%',' ','#']):
        words = list(filter(None,words))
        IN[words[0]] = words[1]
    #changing values
    for i in range(len(par)):
        IN[par[i]]=str(vals[i])
    outfile=open(dest,'w')
    for key, value in IN.items():
        if key not in ('DV_VALUE' , 'DV_PARAM'):
            outfile.write("%s= %s\n"%(key,value))
    outfile.write("%s= %s\n" % ('DV_PARAM', IN['DV_PARAM']))
    outfile.write("%s= %s\n" % ('DV_VALUE', IN['DV_VALUE']))
    #outfile.write('DV_KIND= HICKS_HENNE\nDV_PARAM= ( 0.0, 0.05)\nDEFINITION_DV= ( 1 , 1.0 | wall1,wall2  | 0.0 , 0.05  )\nNUMBER_PART= 8\nWRT_CSV_SOL= YES\nGRADIENT_METHOD= DISCRETE_ADJOINT\nDV_MARKER= ( WING )\nDV_VALUE= 0.001')

def WriteSU2ConfigFile(ConfigName,TYPE):
    with open(ConfigName, 'r') as myfile:
        if TYPE == ("SU2_CFD_AD"or"SU2_DOT_AD"):
            data=myfile.read().replace('MATH_PROBLEM= DIRECT', 'MATH_PROBLEM= DISCRETE_ADJOINT')
        elif TYPE == ("SU2_DEF"):
            pass
        else:
            pass


def ReadUserInput(name, section = None):
    IN = {}
    infile = open(name, 'r')
    for line in infile:
      words = re.split('=| |\n|,|[|]',line)
      if not any(words[0] in s for s in ['\n', '%', ' ', '#']):
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
    IN['Config_Path'] = name
    if section is None:
        return IN
    else:
        length = len(IN['x_leading']) 
        for key, value in IN.items():
            if type(value) == list and len(value)==length:
                IN[key] = np.take(value, section)
        return IN

def WriteBladeConfigFile(name,IN):
    for key in IN:
        input = str(list(IN[key])) if type(IN[key]) == np.ndarray else str(IN[key])
        output = input.replace('[','')
        output1 = output.replace(']', '')
        name.write("%s=%s\n"%(key,output1))

def ConfigPasser(config):
    '''Takes in a path to a config file or directly the parsed dict and returns the parsed dict'''
    if type(config) == str:
        return ReadUserInput(config)
    elif type(config) == dict:
        return config
    else:
        raise TypeError(
            'Inappropriate argument type: input must be path to cfg or the corresponding dictionary itself'
            )

def Numpize(config):
    if type(config['x_leading']) is not np.ndarray:
        for key in param_list:
            config[key] = np.array(config[key]) 
    return config

def Scale(IN, scale=1e-3, in_place=False):
    config = IN if in_place else copy.deepcopy(IN)

    config["SCALE_FACTOR"] = scale
    for key in meridional_channel_names[:5]:
        config[key] = config[key]*config["SCALE_FACTOR"]

    return config

def DeScale(IN, in_place=False):
    config = IN if in_place else copy.deepcopy(IN)

    for key in meridional_channel_names[:5]:
        config[key] = config[key]/config["SCALE_FACTOR"]
    config["SCALE_FACTOR"] = 1

    return config

def Position(IN, le, te, in_place=False):
    config = IN if in_place else copy.deepcopy(IN)

    config["x_leading"] = np.array([le[2]])
    config["y_leading"] = np.array([le[0]])
    config["z_leading"] = np.array([le[1]])
    config["x_trailing"]= np.array([te[2]])
    config["z_trailing"]= np.array([te[1]])

    return config

def Angles(IN, le, te, in_place=False):
    config = IN if in_place else copy.deepcopy(IN)

    vect = te[[2, 0]]-le[[2, 0]]

    config['stagger'] = -np.arccos(
        np.dot([1, 0], vect)/np.linalg.norm(vect)
    )
    config['stagger'] = np.rad2deg(config['stagger'])
    config['theta_in'] = config['stagger']-5
    config['theta_out'] = config['stagger']+5

    for key in ['stagger', 'theta_in', 'theta_out']:
        config[key] = np.array([config[key]])

    return config


# NOTE Likely not needed anymore

# def ConfigCorrector(input_file, output_file):
#     with open(input_file, 'r') as f:
#         data = f.readlines()
#     for i, elem in enumerate(data):
#         data[i] = elem.lstrip()
#         data[i] = ' '.join(elem.split())

#     for i, line in enumerate(data):
#         if '=' not in line:
#             data[i] = data[i]+' '
#         else:
#             data[i] = '\n\n'+data[i]+' '
#         data[i] = data[i].replace('= ', '=').replace(' ', ', ')
#     data = ''.join(data)
#     data = data.replace(', \n', '\n')
#     with open(output_file, 'w') as f:
#         f.write(data)

blade_section_camber_thickness = [
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

meridional_channel_names = [
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

param_list = meridional_channel_names[:5]

param_list.extend(blade_section_camber_thickness)


def ConcatenateConfig(*configs, verbose = True):
    """Concatenates config files in order."""

    if len(configs) != 1:
        for config in configs[1:]:
            for key in param_list:
                configs[0][key] = np.hstack((configs[0][key], config[key]))

    if verbose:
        print('\n\n')
        for key in param_list:
            print(f'\t{key}\t has {configs[0][key].shape[0]} parameters')
        print('\n\n')

    return configs[0]
