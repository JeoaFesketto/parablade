from ssl import SSLSyscallError
import parablade as pb
import matplotlib.pyplot as plt
from parablade.blade_3D import Blade3D
from parablade.blade_2D_camber_thickness import Blade2DCamberThickness
from parablade.blade_plot import BladePlot

blade = Blade3D('./testing/scale_testing/Aachen_2D_2.0.cfg')
blade.make_blade()
blade.set_origin(x = 0, y = 0)
blade.transform(scale = 3, rotate = 90)
blade.transform(rotate = 30)
blade.set_chord(1)
blade.set_pitch(0)
plot = BladePlot(blade)
plot.make_plots()
