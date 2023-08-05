#!/usr/bin/env python
"""
Utility to convert between VTR and SEG-Y formats
------------------------------------------------

Converts <filename> to/from VTR/SEGY depdnding on extension

`vtrconvert file.vtr` writes out a SEG-Y model file `file.sgy`

`vtrconvert file.sgy 10 20 30` (or .segy) writes out a VTR model file `file.vtr`
(for a model with nx1=10, nx2=20, nx3=30)

When converting from SEG-Y to VTR files, you must specify the model size


Usage:
    vtrconvert <filename> [<nx1> <nx2> <nx3>]

Options:
    -h --help       Show this help

"""
from __future__ import print_function, unicode_literals, absolute_import, division

from .. import vtrfile_to_segymodefile, segymodelfile_to_vtrfile
from .. import __version__ as ver
import docopt
import os


def main():
    args = docopt.docopt(__doc__, version=ver)

    filename = args["<filename>"]
    file_basename, file_ext = os.path.splitext(filename)
    if file_ext == ".vtr":
        filename_out = file_basename + ".sgy"
        print("Converting {} to {} ...".format(filename, filename_out))
        vtrfile_to_segymodefile(filename, filename_out)
    elif file_ext == ".sgy" or file_ext == ".segy":
        if not args["<nx1>"]:
            raise ValueError("Require <nx1> when converting from SEG-Y files")
        if not args["<nx2>"]:
            raise ValueError("Require <nx2> when converting from SEG-Y files")
        if not args["<nx3>"]:
            raise ValueError("Require <nx3> when converting from SEG-Y files")
        dims = (int(args["<nx1>"]), int(args["<nx2>"]), int(args["<nx3>"]))
        filename_out = file_basename + ".vtr"
        print("Converting {} to {} ...".format(filename, filename_out))
        segymodelfile_to_vtrfile(filename, filename_out, dims)
    else:
        raise ValueError("unrecognized file extension")


if __name__ == "__main__":
    main()
