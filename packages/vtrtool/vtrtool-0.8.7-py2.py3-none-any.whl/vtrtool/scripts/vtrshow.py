#!/usr/bin/env python
"""
Simple 3D slice viewer for VTR models
------------------------------------------------

When viewing SEG-Y files, you must specify the model size

Usage:
    vtrconvert <filename> [<nx1> <nx2> <nx3>]

Options:
    -h --help       Show this help

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import os

import docopt
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from .. import VTRModel
from .. import __version__ as ver
from .. import segymodelfile_to_vtrmodel


def _handle_filetype(filename, read_model=True, dims=None):
    # Returns a VTRModel object from a file
    _, file_ext = os.path.splitext(filename)
    if file_ext == ".vtr":
        return VTRModel(filename, read_model=read_model)
    elif file_ext == ".sgy" or file_ext == ".segy":
        return segymodelfile_to_vtrmodel(filename, dims=dims)
    else:
        raise ValueError("unrecognized file extension")


def vtrshow(cube, axis=1, **kwargs):
    """
    Display a 3d ndarray with a slider to move along the third dimension.

    Extra keyword arguments are passed to imshow
    """

    # check dim
    if not cube.ndim == 3:
        raise ValueError("cube should be an ndarray with ndim == 3")

    # generate figure
    fig = plt.figure()
    ax = plt.subplot(111)
    fig.subplots_adjust(left=0.25, bottom=0.25)

    # select first image
    s = [slice(0, 1) if i == axis else slice(None) for i in range(3)]
    im = cube[tuple(s)].squeeze().transpose()

    # display image
    image_handle = ax.imshow(im, **kwargs)

    # define slider
    ax = fig.add_axes([0.25, 0.1, 0.65, 0.03])

    slider = Slider(
        ax, "Axis %i index" % axis, 0, cube.shape[axis] - 1, valinit=0, valfmt="%i"
    )

    def update(val):
        ind = int(slider.val)
        s = [slice(ind, ind + 1) if i == axis else slice(None) for i in range(3)]
        im = cube[tuple(s)].squeeze().transpose()
        image_handle.set_data(im, **kwargs)
        fig.canvas.draw()

    slider.on_changed(update)
    plt.show()


def main():
    args = docopt.docopt(__doc__, version=ver)
    if args["<nx1>"] and args["<nx2>"] and args["<nx3>"]:
        dims = (int(args["<nx1>"]), int(args["<nx2>"]), int(args["<nx3>"]))
    else:
        dims = None
    vtr = _handle_filetype(args["<filename>"], dims=dims)
    vtrshow(vtr.arrays[0])


if __name__ == "__main__":
    main()
