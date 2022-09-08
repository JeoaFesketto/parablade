import parablade as pb
import numpy as np
import matplotlib.pyplot as plt

from parablade.common.config import ReadUserInput

# details_dict = pb.ReadUserInput(r'./testcases/MatchBlades/Aachen_2D/Aachen_2D.cfg')
# o = pb.BladeMatch(details_dict)
# o.match_blade(matching_mode='DVs')

# print(ReadUserInput(r'./output_matching/matched_parametrization.cfg'))

o = pb.Blade2DCamberThickness(r'./output_matching/matched_parametrization.cfg')
o.plot_blade_section()
plt.show()

