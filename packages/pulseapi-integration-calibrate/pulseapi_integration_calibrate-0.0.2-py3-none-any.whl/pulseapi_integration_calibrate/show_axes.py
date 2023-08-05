# Показывает оси базы и смещенной системы координат. Задавать точки осей вручнуую!!!!
from matplotlib import pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
arrow_prop_dict = dict(mutation_scale=20, arrowstyle='->', shrinkA=0, shrinkB=0)

a = Arrow3D([0, 1], [0, 0], [0, 0], **arrow_prop_dict, color='r')
ax.add_artist(a)
a = Arrow3D([0, 0], [0, 1], [0, 0], **arrow_prop_dict, color='b')
ax.add_artist(a)
a = Arrow3D([0, 0], [0, 0], [0, 1], **arrow_prop_dict, color='g')
ax.add_artist(a)

# p0 = [-0.28, -0.07, 0.326]
# px = [-1.279934250235642, -0.07917370871775817, 0.31911971846168136]
# py = [-0.29123070169772836, 0.5922422907598568, 1.075205592390042]
# pz = [-0.2776834195327072, -0.8192336026884397, 0.9883017756713623]
b = Arrow3D([p0[0], px[0]], [p0[1], px[1]], [p0[2], px[2]], **arrow_prop_dict, color='r')
ax.add_artist(b)
b = Arrow3D([p0[0], py[0]], [p0[1], py[1]], [p0[2], py[2]], **arrow_prop_dict, color='b')
ax.add_artist(b)
b = Arrow3D([p0[0], pz[0]], [p0[1], pz[1]], [p0[2], pz[2]], **arrow_prop_dict, color='g')
ax.add_artist(b)

# ax.text(0.0, 0.0, -0.1, r'$o$')
# ax.text(1.1, 0, 0, r'$x$')
# ax.text(0, 1.1, 0, r'$y$')
# ax.text(0, 0, 1.1, r'$z$')

ax.view_init(azim=-90, elev=90)
ax.set_axis_off()
plt.show()
