import parablade as pb
import matplotlib.pyplot as plt
from parablade.blade_3D import Blade3D
from parablade.blade_2D_camber_thickness import Blade2DCamberThickness
from parablade.blade_plot import BladePlot

blade = Blade3D('/home/daep/j.fesquet/git_repos/parablade/testcases/MatchBlades/Aachen_2D/Aachen_2D.cfg')
blade.make_blade()

blade.set_leading_edge(0, 0)
plot1 = BladePlot(blade)
plot1.make_plots()
blade.scale(1.5)
plot = BladePlot(blade)
plot.make_plots()
plt.show()
