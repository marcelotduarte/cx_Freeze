"""A collection of functions which are triggered automatically by finder when
scikit-image package is included.
"""

from __future__ import annotations

from ..finder import ModuleFinder
from ..module import Module


def load_skimage(finder: ModuleFinder, module: Module) -> None:  # noqa: ARG001
    """The skimage package."""
    finder.include_package("skimage.io")
    # exclude all tests
    finder.exclude_module("skimage.color.tests")
    finder.exclude_module("skimage.data.tests")
    finder.exclude_module("skimage.draw.tests")
    finder.exclude_module("skimage.exposure.tests")
    finder.exclude_module("skimage.feature.tests")
    finder.exclude_module("skimage.filters.tests")
    finder.exclude_module("skimage.graph.tests")
    finder.exclude_module("skimage.io.tests")
    finder.exclude_module("skimage.measure.tests")
    finder.exclude_module("skimage.metrics.tests")
    finder.exclude_module("skimage.morphology.tests")
    finder.exclude_module("skimage.restoration.tests")
    finder.exclude_module("skimage.segmentation.tests")
    finder.exclude_module("skimage._shared.tests")
    finder.exclude_module("skimage.transform.tests")
    finder.exclude_module("skimage.util.tests")
    finder.exclude_module("skimage.viewer.tests")


def load_skimage_feature_orb_cy(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The skimage.feature.orb_cy is an extension that load a module."""
    finder.include_module("skimage.feature._orb_descriptor_positions")
