import parablade as pb
from parablade.blade_3D import Blade3D
from parablade.blade_plot import BladePlot

blade = Blade3D('testcases/MatchBlades/Aachen_2D/Aachen_2D.cfg')
blade.make_blade()
plot = BladePlot(blade)
plot.make_interactive_plot()