import parablade as pb
from parablade.blade_3D import Blade3D
from parablade.blade_2D_camber_thickness import Blade2DCamberThickness
from parablade.blade_plot import BladePlot

# sans modifications

blade = Blade3D('testcases/MatchBlades/Aachen_3D/Aachen_3D.cfg')
blade.make_blade()
plot = BladePlot(blade)
plot.make_plots()


# avec modifications

blade = Blade3D('/home/daep/j.fesquet/git_repos/parageom/example_files/moded_aachen.cfg')
blade.make_blade()
plot = BladePlot(blade)
plot.make_plots()