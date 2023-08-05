"""
Command line output of information on Mitiq and dependencies.
"""
__all__ = ['about']

import sys
import os
import platform
import numpy
import mitiq
import inspect

def about():
    """
    About box for Mitiq. Gives version numbers for mitiq, NumPy.
    """
    print("")
    print("Mitiq: A Python toolkit for implementing ")
    print("error mitigation on quantum computers.")
    print("========================================")
    print("Mitiq team – 2020 and later.")
    print("https://unitary.fund")
    print("")
    print("mitiq Version:      %s" % mitiq.__version__)
    print("Numpy Version:      %s" % numpy.__version__)
    print("Python Version:     %d.%d.%d" % sys.version_info[0:3])
    print("Platform Info:      %s (%s)" % (platform.system(),
                                           platform.machine()))
    mitiq_install_path = os.path.dirname(inspect.getsourcefile(mitiq))
    print("Installation path:  %s" % mitiq_install_path)

if __name__ == "__main__":
    about()