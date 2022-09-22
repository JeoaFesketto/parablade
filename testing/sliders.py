import parablade as pb
import numpy as np
import matplotlib.pyplot as plt
import sys

from parablade.common.config import ReadUserInput

details_dict = ReadUserInput('testcases/MatchBlades/Aachen_2D/Aachen_2D.cfg')
o = pb.BladeMatch(details_dict, 
        plot_options={
            "view_xy": "yes",
            "view_xR": "no",
            "view_yz": "no",
            "view_3D": "no",
            "error_distribution": "yes"

        }, coarseness=1)
o.match_blade(matching_mode='manual_sliders')

