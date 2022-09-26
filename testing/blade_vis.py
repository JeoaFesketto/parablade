import parablade as pb
import matplotlib.pyplot as plt
from parablade.blade_3D import Blade3D
from parablade.blade_2D_camber_thickness import Blade2DCamberThickness
from parablade.blade_plot import BladePlot

blade = Blade3D('/home/daep/j.fesquet/git_repos/parageom/confidential/dgen_param.cfg')
blade.make_blade()

print(blade.surface_coordinates.shape)
curve = blade.surface_coordinates.T

ax = plt.axes(projection="3d")
ax.plot3D(curve.T[1], curve.T[0], curve.T[2], "gray")

ax.set_xlim(-100, 30)
ax.set_zlim(0, 180)
ax.set_ylim(-250, 200)
ax.set_box_aspect(
    [ub - lb for lb, ub in (getattr(ax, f"get_{a}lim")() for a in "xyz")]
)

plt.show()