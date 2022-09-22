import parablade as pb
import numpy as np
import matplotlib.pyplot as plt
import sys

from parablade.common.config import ReadUserInput

details_dict = ReadUserInput('./my_tests/dgen_param.cfg')
o = pb.BladeMatch(details_dict, 
        plot_options={
            "view_xy": "yes",
            "view_xR": "yes",
            "view_yz": "no",
            "view_3D": "yes",
            "error_distribution": "yes"

        }, coarseness=1)
o.match_blade(matching_mode='DVs')

