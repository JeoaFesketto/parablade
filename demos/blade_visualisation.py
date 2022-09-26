import parablade as pb
import matplotlib.pyplot as plt
from parablade.blade_3D import Blade3D
from parablade.blade_2D_camber_thickness import Blade2DCamberThickness
from parablade.blade_plot import BladePlot

blade = Blade3D('testing/scale_testing/Aachen_2D_2.0.cfg')
blade.make_blade()
blade.set_origin(x = -10, y = 40)
blade.transform(dx = 10, rotate = 180, scale = 10)
plot = BladePlot(blade)
plot.make_plots()

# blade.set_leading_edge(0, 0)
# plot1 = BladePlot(blade)
# plot1.make_plots()
# print(blade.IN)
# blade.scale(2)
# print(blade.IN)
# plot = BladePlot(blade)
# plot.make_plots()
# plt.show()
