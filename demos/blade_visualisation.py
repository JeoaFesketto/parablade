from ssl import SSLSyscallError
import parablade as pb
import matplotlib.pyplot as plt
from parablade.blade_3D import Blade3D
from parablade.blade_2D_camber_thickness import Blade2DCamberThickness
from parablade.blade_plot import BladePlot

blade = Blade3D('/home/daep/j.fesquet/git_repos/parageom/confidential/dgen_param.cfg')
blade.make_blade()
blade.set_origin(x = 0, y = 0)
blade.set_chord(1)
blade.set_pitch(0)
plot = BladePlot(blade)
plot.make_plots()
