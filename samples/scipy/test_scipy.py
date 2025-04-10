"""A simple script to demonstrate scipy."""

import numpy as np
import scipy
from scipy.spatial.transform import Rotation

if __name__ == "__main__":
    print("numpy version", np.__version__)
    print("scipy version", scipy.__version__)
    print(Rotation.from_euler("XYZ", [10, 10, 10], degrees=True).as_matrix())
