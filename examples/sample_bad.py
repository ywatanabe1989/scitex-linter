#!/usr/bin/env python3
"""Sample script with SciTeX lint issues — for demonstration."""

import matplotlib.pyplot as plt  # STX-I001: use stx.plt
import numpy as np

# STX-S001: missing @stx.session
# STX-S005: missing import scitex as stx


def main():
    # STX-PA004: os.chdir detected
    import os

    os.chdir("/tmp")

    # STX-PA001: absolute path
    np.save("/tmp/data.npy", [1, 2, 3])

    # STX-IO007: plt.savefig
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3])
    plt.savefig("plot.png")

    # STX-P004: plt.show
    plt.show()

    print("done")  # STX-P005: use logger


# STX-S002: missing __main__ guard
main()
