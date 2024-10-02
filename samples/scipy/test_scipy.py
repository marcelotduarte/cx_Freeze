"""A simple script to demonstrate scipy."""

from scipy.spatial.transform import Rotation

if __name__ == "__main__":
    print(Rotation.from_euler("XYZ", [10, 10, 10], degrees=True).as_matrix())
