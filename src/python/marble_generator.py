import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
N = 201


x = np.linspace(-1, 1, N)
y = np.linspace(-1, 1, N)
xx, yy = np.meshgrid(x, y)

for i in range(4*8*2):
    params = (np.random.rand(5) - 0.5) * 0.4

    mat = 2-(xx**2 + yy**2)

    mat -= xx**2*params[0] + yy**2*params[1] + xx*yy*params[2]


    mat -= 0.2

    mat_mask = mat.copy()

    mat += xx*params[3] + yy*params[4]

    mat[mat_mask < 1] = np.NaN

    color1 = np.random.rand(3) * 0.3
    color2 = np.random.rand(3) * 0.6
    colors = [color1, color2]
    cmap = LinearSegmentedColormap.from_list("mycmap", colors)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(mat, cmap=cmap)
    ax.axis(False)
    fig.tight_layout()
    fig.savefig("marbles_large/{}.png".format(i), dpi=N/5, transparent=True)
