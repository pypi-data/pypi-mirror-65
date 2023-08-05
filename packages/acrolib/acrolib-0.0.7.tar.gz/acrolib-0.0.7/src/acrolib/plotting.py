import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

def get_default_axes3d(xlim=[-1, 1], ylim=[-1, 1], zlim=[-1, 1]):
    """ Create a default `mpl_toolkits.mplot3d.Axes3D` object with default
    axis limits on all axis from -1 to 1, and labels on the axes.
    """
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    ax.set_xlim3d(xlim)
    ax.set_ylim3d(ylim)
    ax.set_zlim3d(zlim)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    return fig, ax


def plot_reference_frame(ax, tf=None, arrow_length=0.2):
    """ Plot xyz-axes on axes3d object
    Parameters
    ----------
    ax : mpl_toolkits.mplot3d.Axes3D
        Axes object for 3D plotting.
    tf : np.array of float
        Transform to specify location of axes. Plots in origin if None.
    l : float
        The length of the axes plotted.
    """
    l = arrow_length
    x_axis = np.array([[0, l], [0, 0], [0, 0]])
    y_axis = np.array([[0, 0], [0, l], [0, 0]])
    z_axis = np.array([[0, 0], [0, 0], [0, l]])

    if tf is not None:
        # rotation
        x_axis = np.dot(tf[:3, :3], x_axis)
        y_axis = np.dot(tf[:3, :3], y_axis)
        z_axis = np.dot(tf[:3, :3], z_axis)
        # translation [:, None] numpian way to change shape (add axis)
        x_axis = x_axis + tf[:3, 3][:, None]
        y_axis = y_axis + tf[:3, 3][:, None]
        z_axis = z_axis + tf[:3, 3][:, None]

    ax.plot(x_axis[0], x_axis[1], x_axis[2], "-", c="r")
    ax.plot(y_axis[0], y_axis[1], y_axis[2], "-", c="g")
    ax.plot(z_axis[0], z_axis[1], z_axis[2], "-", c="b")
