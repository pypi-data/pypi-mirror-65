# Licensed under ...
"""
This is the top level module from which functions and classes of
Mitiq can be directly imported.
"""
import os
from typing import Union

_directory_of_this_file = os.path.dirname(os.path.abspath(__file__))


with open(str(_directory_of_this_file) + "/../VERSION.txt", "r") as f:
    __version__ = f.read().strip()

def version():
    """Returns the Mitiq version number."""
    return __version__
