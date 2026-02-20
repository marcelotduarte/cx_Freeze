**cx_Freeze** Creates standalone executables from Python scripts with the same
performance as the original script.

It is cross-platform and should work on any platform that Python runs on.

# Version 8.6 (2026-02-20)

# Version 8.5 (2025-11-24)

- Separation into two distinct packages: cx_Freeze and freeze-core
- Support for Python 3.14 and 3.14t (cx_Freeze and freeze-core)
- Add support for Python 3.13t on Windows (freeze-core)
- Add support for bdist_msi on Python 3.13 and 3.14 (python-msilib)
- bdist_msi - fix for initial_target_dir and target_name
- bdist_appimage - add runtime_file, sign, sign_key and updateinformation
  options.
- bdist_appimage - add support for 'gui' app in desktop file
- Apply security best practices
- Fix a performance bug (optimized implementation of '\_find_editable_spec')
- Refactor finder scan code
- Drop Python 3.9 support
- Bug fixes, hooks, and tests.

# Version 8.4 (2025-08-11)

- Refactor dynamic libraries finder.
- Bug fixes, hooks, and tests.

# Version 8.3 (2025-05-11)

- Experimental support for Python 3.11 to 3.13 on Windows ARM64 (win_arm64).
- Bug fixes, hooks, and more tests.

# Version 8.2 (2025-04-22)

- Make MSI checkbox to "launch on finish" optional.
- Bug fixes, hooks, and more tests.

# Version 8.1 (2025-04-02)

- Add "launch on finish" checkbox to the MSI installer.
- Bug fixes and improvements (including hook additions and enhancements).

# Version 8.0 (2025-03-21)

- Python 3.13 support.
- Experimental support for Python 3.13 free-threaded on Linux and macOS.
- Download and extract the [MSVC Redistributable files](https://cx-freeze.readthedocs.io/en/stable/faq.html#microsoft-visual-c-redistributable-package).
- Implement bases using PEP587 - Python Initialization Configuration.
- Drop Python 3.8 support.
- Bug fixes and improvements (including hook additions and enhancements).

# Version 7.2 (2024-07-16)

- Improved bdist_dmg
- Add license for msi (bdist_msi)
- Minor improvements in bdist_appimage
- Drop rpm2_mode in bdist_rpm
- Use an optimized mode as default for pip installations of selected packages
- hooks: support numpy 2.0, rasterio, multiprocess (a multiprocessing fork), etc
- Regression fixes, bug fixes and improvements

# Version 7.1 (2024-05-26)

- Added new option --zip-filename in build_exe
- Bug fixes and improvements

# Version 7.0 (2024-04-21)

- Added support for pyproject.toml
- Create Linux AppImage format: bdist_appimage
- Create an DEB distribution: bdist_deb
- Improved bdist_mac
- New and updated hooks, including support for QtWebengine on macOS
- Python 3.12 support.
- Improved tests and coverage ( >80% ).
- Bug fixes and improvements

# Version 6.15 (2023-05-23)

- Breaking change: remove camelCase in Executable api
- New hooks: lazy_loader, librosa, jpype, pyimagej, pyreadstat
- Improved hooks: matplotlib, pytorch, PyQt6, PySide6, TkInter
- Bug fixes and improvements

# Version 6.14 (2023-01-24)

- Support Python 3.11
- Binary wheels (x86_64 and aarch64) for musllinux
- Maintain Windows base executables on git (install from sources without C compiler)
- Improved documentation
- New hooks: charset_normalizer, shapely, sklearn, pytorch
- Improved hooks: scipy, sqlite3
- Bug fixes and improvements

# Version 6.13 (2022-10-26)

- New hooks for PyQt6 (6.3.1 and 6.4.0)
- Improved hooks to support new PySide6 6.4.0
- Bug fixes and improvements

# Version 6.12 (2022-10-02)

- Improve tkinter hook to work on all OS
- Improved PyQt5/Pyside2 hooks and new hook for PySide6
- Linux binary wheels for arm64 (aarch64)
- Bug fixes and improvements

# Version 6.11 (2022-06-04)

- Binary wheels for manylinux and macOS (including Apple Silicon)
- Complete integration to use setuptools instead of distutils
- More code modernization
- Bug fixes and improvements

# Version 6.10 (2022-01-24)

- Support Application Manifests in Windows: manifest and uac-admin
- EXPERIMENTAL New dependency resolver on Windows
- EXPERIMENTAL Support for Apple Silicon using miniforge (conda-forge)
- Bug fixes and improvements

# Version 6.2 up to 6.9 (2020-07-09 to 2021-12-07)

- Support for pathlib.Path
- New or improved hooks, with emphasis on matplotlib, numpy, PyQt5 and PySide2
- New ModuleFinder engine uses importlib.machinery
- Refactored Freezer
- New support for package metadata improving Module and new DitributionCache
- Enhanced support for Python 3.8 and Python 3.9, including MSYS2 and Anaconda distributions
- Improvements for multiprocessing
- Optimizations in detection and distribution of libraries
- Integrated to setuptools and importlib-metadata
- Code modernization
- Various bug fixes.
