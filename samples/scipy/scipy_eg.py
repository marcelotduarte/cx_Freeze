"""A simple script to demonstrate scipy."""

from scipy.stats import norm


if __name__ == "__main__":
    print("bounds of distribution lower: %s, upper: %s" % norm.support())
