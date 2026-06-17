"""Internal _metadata module."""

from __future__ import annotations

import re
from importlib.machinery import EXTENSION_SUFFIXES
from importlib.metadata import PathDistribution
from importlib.metadata import version as metadata_version
from pathlib import Path
from typing import TYPE_CHECKING

from packaging.requirements import Requirement

from cx_Freeze._compat import IS_MINGW, IS_WINDOWS
from cx_Freeze.exception import ModuleError

if TYPE_CHECKING:
    from cx_Freeze._typing import StrPath
    from cx_Freeze.finder import ModuleFinder

__all__ = ["DistributionCache"]


class DistributionCache(PathDistribution):
    """Cache the distribution package."""

    def __init__(self, name: str, finder: ModuleFinder) -> None:
        """Construct a distribution.

        :param name: The name of the distribution package to cache.
        :param finder: The ModuleFinder object where the distribution
        metadata are cached.
        :raises ModuleError: When the named package's distribution
            metadata cannot be found.
        """
        try:
            distribution = finder.import_distributions[name]
        except KeyError:
            raise ModuleError(name) from None
        self._dist = distribution
        self._name = name

        # Cache dist-info files in a temporary directory
        normalized_name = self.normalized_name
        source_path = getattr(distribution, "_path", None)
        if source_path is None:
            dist_path = Path(str(distribution.locate_file(".")))
            for expected_name in (normalized_name, name, distribution.name):
                mask = f"{expected_name}-{distribution.version}.*-info"
                source_path = next(dist_path.glob(mask), None)
                if source_path is not None:
                    break
        if source_path is None or not source_path.exists():
            raise ModuleError(name)
        dist_name = f"{normalized_name}-{distribution.version}.dist-info"
        target_path = finder.cache_path / dist_name
        super().__init__(target_path)
        self.distinfo_name = dist_name
        if target_path.exists():  # already cached
            return

        # Copy data from dist-info directory or create it.
        target_path.mkdir(parents=True)
        purelib = False
        if source_path.name.endswith(".dist-info"):
            for source in source_path.rglob("*"):
                target = target_path / source.relative_to(source_path)
                if source.is_dir():
                    target.mkdir(exist_ok=True)
                else:
                    target.write_bytes(source.read_bytes())
        elif source_path.is_file():
            # old egg-info file is converted to dist-info
            target = target_path / "METADATA"
            target.write_bytes(source_path.read_bytes())
            purelib = bool(
                source_path.parent.joinpath(normalized_name + ".py").exists()
            )
        else:
            # Copy minimal data from egg-info directory into dist-info
            source = source_path / "PKG-INFO"
            if source.is_file():
                target = target_path / "METADATA"
                target.write_bytes(source.read_bytes())
            source = source_path / "entry_points.txt"
            if source.is_file():
                target = target_path / "entry_points.txt"
                target.write_bytes(source.read_bytes())
            source = source_path / "top_level.txt"
            if source.is_file():
                target = target_path / "top_level.txt"
                target.write_bytes(source.read_bytes())
            purelib = not bool(source_path.joinpath("not-zip-safe").is_file())

        self._write_wheel_distinfo(purelib)
        self._write_record_distinfo()

    @property
    def name(self) -> str:
        return self._dist.metadata["Name"]

    @property
    def normalized_name(self) -> str:
        return getattr(
            self._dist, "_normalized_name", self.name.lower().replace("-", "_")
        )

    def _write_wheel_distinfo(self, purelib: bool) -> None:
        """Create a WHEEL file if it doesn't exist."""
        target = self.locate_file(f"{self.distinfo_name}/WHEEL")
        if not target.exists():
            project = Path(__file__).parent.name  # cx_Freeze
            version = metadata_version(project)
            root_is_purelib = "true" if purelib else "false"
            text = [
                "Wheel-Version: 1.0",
                f"Generator: {project} ({version})",
                f"Root-Is-Purelib: {root_is_purelib}",
                "Tag: py3-none-any",
            ]
            with target.open(mode="w", encoding="utf_8", newline="") as file:
                file.write("\n".join(text))

    def _write_record_distinfo(self) -> None:
        """Recreate a minimal RECORD file."""
        distinfo_name = self.distinfo_name
        target = self.locate_file(f"{distinfo_name}/RECORD")
        target_dir = target.parent
        record = [
            f"{distinfo_name}/{file.name},," for file in target_dir.iterdir()
        ]
        record.append(f"{distinfo_name}/RECORD,,")
        with target.open(mode="w", encoding="utf_8", newline="") as file:
            file.write("\n".join(record))

    @property
    def binary_files(self) -> list[str]:
        """Return the relative path of binary files included in the package."""
        files = self._dist.files
        if not files:
            return []

        if IS_MINGW or IS_WINDOWS:
            # all .dll's
            return [
                file.as_posix()
                for file in files
                if file.suffix.lower() == ".dll"
            ]

        # Linux and macOS
        extensions = tuple([ext for ext in EXTENSION_SUFFIXES if ext != ".so"])
        # all .so* or .dylib as long as it is not a python extension
        return [
            file.as_posix()
            for file in files
            if (file.match("*.so*") or file.match("*.dylib"))
            and not file.name.endswith(extensions)
        ]

    @property
    def installer(self) -> str:
        """Return the installer (pip, conda) for the distribution package."""
        # consider 'uv' as 'pip'
        value = self.read_text("INSTALLER") or "pip"
        return value.splitlines()[0].replace("uv", "pip")

    def locate_file(self, path: StrPath) -> Path:
        """Given a path to a file in this distribution, return a path to it."""
        if Path(path).parents[0].as_posix() == self.distinfo_name:
            full_path = super().locate_file(path)
        else:
            full_path = self._dist.locate_file(path)
        return Path(str(full_path)).resolve()

    @property
    def requires(self) -> list[str]:
        """Generated requirements specified for this Distribution."""
        package_names = []
        requires = super().requires
        if requires:
            for requirement_string in requires:
                require = Requirement(requirement_string)
                if require.marker is None or require.marker.evaluate():
                    package_names.append(require.name)
        return package_names

    @property
    def version(self) -> tuple[str | int, ...]:
        """Return the 'Version' metadata for the distribution package."""
        version_separators = re.compile(r"[\._-]")
        version_value = super().version or ""
        return tuple(
            part.lower() if not part.isdigit() else int(part)
            for part in version_separators.split(version_value)
        )
