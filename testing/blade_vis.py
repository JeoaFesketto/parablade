import parablade as pb
from parablade.blade_3D import Blade3D
from parablade.blade_plot import BladePlot

blade = Blade3D('/home/daep/j.fesquet/git_repos/parageom/confidential/dgen_param.cfg')
blade.make_blade()
plot = BladePlot(blade)
plot.make_interactive_plot()