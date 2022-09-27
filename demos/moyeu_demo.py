import parablade as pb
from parablade.blade_3D import Blade3D
from parablade.blade_2D_camber_thickness import Blade2DCamberThickness
from parablade.blade_plot import BladePlot

# sans modifications

blade = Blade3D('testcases/MatchBlades/Aachen_3D/hub_demo.cfg')
blade.make_blade()
plot = BladePlot(blade)
plot.make_plots()
