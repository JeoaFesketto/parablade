import parablade as pb
import numpy as np
import matplotlib.pyplot as plt



o = pb.Blade2DCamberThickness(r'./output_matching/matched_parametrization.cfg')
o.plot_blade_section()
plt.show()

