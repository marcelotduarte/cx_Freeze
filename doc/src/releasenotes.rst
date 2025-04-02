Release notes
=============

.. toctree::
   :maxdepth: 2
   :hidden:

   releasenotes-7x.rst
   releasenotes-6x.rst
   releasenotes-5x.rst

8.x releases
############

Version 8.1 (Apr 02)
--------------------

#)  Bump version: 8.0.0 → 8.1.0 [ci skip] (:pull:`2868`) :user:`marcelotduarte`
#)  chore: support for setuptools fix for pep491 (:pull:`2867`) :user:`marcelotduarte`
#)  build(deps): bump pytest-cov from 6.0.0 to 6.1.0 (:pull:`2866`) :user:`dependabot`
#)  build(deps): bump sphinx-new-tab-link from 0.7.0 to 0.8.0 (:pull:`2865`) :user:`dependabot`
#)  hooks: fix scipy (using numpy) (:pull:`2862`) :user:`marcelotduarte`
#)  bdist_msi: Add a launch on finish checkbox to the MSI installer (:pull:`2854`) :user:`MeGaGiGaGon`
#)  build(deps): bump coverage from 7.7.1 to 7.8.0 (:pull:`2864`) :user:`dependabot`
#)  hooks: include source files that uses @torch.jit._overload_method (:pull:`2863`) :user:`marcelotduarte`
#)  fix: ruff A005 (:pull:`2859`) :user:`marcelotduarte`
#)  hooks: zlib module requires the zlib.dll to be present in the executable directory [conda/Windows] (:pull:`2855`) :user:`marcelotduarte`
#)  hooks: add argon2-cffi (:pull:`2857`) :user:`marcelotduarte`
#)  fix: ruff LOG015 [ci skip] (:pull:`2858`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.23.1 to 2.23.2 (:pull:`2853`) :user:`dependabot`
#)  hooks: update to support pymupdf 1.25.4 (:pull:`2851`) :user:`marcelotduarte`
#)  hooks: fix importlib hook (:pull:`2852`) :user:`marcelotduarte`
#)  hooks: enable asynchat and asyncore usage via pyasynchat and pyasyncore packages (:pull:`2850`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2849`) :user:`pre-commit-ci`
#)  doc: fix version documentation [ci skip] (:pull:`2847`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 1.0.2 to 1.1.1 (:pull:`2846`) :user:`dependabot`
#)  Update setup_script.rst fixed typo in docs (:pull:`2845`) :user:`philipp`
#)  build(deps): bump coverage from 7.7.0 to 7.7.1 (:pull:`2840`) :user:`dependabot`
#)  fix: use only console based on PEP587 on Python 3.13 (:pull:`2842`) :user:`marcelotduarte`

Version 8.0 (Mar 21)
--------------------

#)  hooks: add timm package (:pull:`2834`) :user:`marcelotduarte`
#)  build(deps-dev): bump pre-commit from 4.1.0 to 4.2.0 (:pull:`2833`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2832`) :user:`pre-commit-ci`
#)  build(deps): bump coverage from 7.6.12 to 7.7.0 (:pull:`2830`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.23.0 to 2.23.1 (:pull:`2831`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2828`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 1.0.1 to 1.0.2 (:pull:`2827`) :user:`dependabot`
#)  build(deps): bump sphinx-new-tab-link from 0.6.1 to 0.7.0 (:pull:`2826`) :user:`dependabot`
#)  build(deps): bump pytest from 8.3.4 to 8.3.5 (:pull:`2818`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.32.1 to 1.0.1 (:pull:`2824`) :user:`dependabot`
#)  build(deps): update lief requirement from <=0.16.3,>=0.13.2 to >=0.13.2,<=0.16.4 (:pull:`2816`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.22.0 to 2.23.0 (:pull:`2819`) :user:`dependabot`
#)  fix: setuptools 75.8.1 breaks auditwheel (:pull:`2823`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2814`) :user:`pre-commit-ci`
#)  build(deps): update myst-parser requirement from <=4.0.0,>=3.0.1 to >=3.0.1,<=4.0.1 (:pull:`2809`) :user:`dependabot`
#)  build(deps): bump coverage from 7.6.11 to 7.6.12 (:pull:`2806`) :user:`dependabot`
#)  build-wheel: use ubuntu 22.04 emulator to build ppc64le (:pull:`2805`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2804`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.32.0 to 0.32.1 (:pull:`2803`) :user:`dependabot`
#)  build(deps): bump coverage from 7.6.10 to 7.6.11 (:pull:`2802`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.31.1 to 0.32.0 (:pull:`2800`) :user:`dependabot`
#)  fix: missing dlls in top directory [mingw] (:pull:`2799`) :user:`marcelotduarte`
#)  hooks: fix shapely [windows] (:pull:`2797`) :user:`marcelotduarte`
#)  build(deps): update lief requirement from <=0.16.2,>=0.13.2 to >=0.13.2,<=0.16.3 (:pull:`2795`) :user:`dependabot`
#)  tests: fix msi test (:pull:`2796`) :user:`marcelotduarte`
#)  doc: fix typo [ci skip] (:pull:`2793`) :user:`marcelotduarte`
#)  doc: improve documentation on using pyproject.toml [ci skip] (:pull:`2792`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.29.0 to 0.31.1 (:pull:`2790`) :user:`dependabot`
#)  hooks: ctypes, ssl, sqlite3 - conda-forge (:pull:`2791`) :user:`marcelotduarte`
#)  chore: support ruff 0.9.x (:pull:`2789`) :user:`marcelotduarte`
#)  hooks: copy only shared libs of Qt in qt hooks (:pull:`2788`) :user:`marcelotduarte`
#)  hooks: pytorch 2.6.0 (:pull:`2787`) :user:`marcelotduarte`
#)  chore: build_wheel improvements and use of ubuntu-24.04-arm runner (:pull:`2784`) :user:`marcelotduarte`
#)  hooks: complementary fix for pytorch/nvidia/torchmetrics (:pull:`2782`) :user:`marcelotduarte`
#)  hooks: fix pytorch on macOS (:pull:`2781`) :user:`marcelotduarte`
#)  build(deps-dev): bump pre-commit from 4.0.1 to 4.1.0 (:pull:`2778`) :user:`dependabot`
#)  fix: work with lief disabled or uninstalled (:pull:`2777`) :user:`marcelotduarte`
#)  appimage: use full path of appimagetool (:pull:`2771`) :user:`marcelotduarte`
#)  chore: lief>=0.13.2,<=0.16.2 [windows] (:pull:`2770`) :user:`marcelotduarte`
#)  chore: use new features of uv (:pull:`2769`) :user:`marcelotduarte`
#)  chore: enable experimental free-threaded python 3.13 on unix (:pull:`2759`) :user:`marcelotduarte`
#)  ci: minor tweaks and fixes (:pull:`2768`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2766`) :user:`pre-commit-ci`
#)  ci: fix some build and test issues (:pull:`2767`) :user:`marcelotduarte`
#)  chore: happy new year [ci skip] (:pull:`2765`) :user:`marcelotduarte`
#)  hooks: fix pyqt5 on conda-forge (:pull:`2763`) :user:`marcelotduarte`
#)  chore: add some fail-safe checks (:pull:`2764`) :user:`marcelotduarte`
#)  fix: #2680 regression (:pull:`2762`) :user:`marcelotduarte`
#)  hooks: update pyqt5/pyqt6/pyside6 resources [ci skip] (:pull:`2761`) :user:`marcelotduarte`
#)  build-wheel: build only universal2 wheels on macOS (:pull:`2760`) :user:`marcelotduarte`
#)  hooks: fix for torch and triton backends (:pull:`2751`) :user:`marcelotduarte`
#)  hooks: fix for pytorch/nvidia/torchmetrics (:pull:`2750`) :user:`marcelotduarte`
#)  doc: Corrects a typo in `setup_script.rst` (:pull:`2757`) :user:`patocv2`
#)  ci: Publish to testpypi does not work on PR on a fork [ci skip] (:pull:`2758`) :user:`marcelotduarte`
#)  hooks: add shapely.py (:pull:`2749`) :user:`marcelotduarte`
#)  bases: update base executables and util module [ci skip] (:pull:`2756`) :user:`marcelotduarte`
#)  build-wheel: use uvx w/ bump-my-version and cibuildwheel (:pull:`2755`) :user:`marcelotduarte`
#)  chore: use pythoncapi_compat (:pull:`2754`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.6.9 to 7.6.10 (:pull:`2752`) :user:`dependabot`
#)  fix: three small fixes (:pull:`2748`) :user:`marcelotduarte`
#)  build-wheel: improve performance (:pull:`2747`) :user:`marcelotduarte`
#)  build(deps): bump astral-sh/setup-uv from 4 to 5 (:pull:`2744`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.28.3 to 0.29.0 (:pull:`2745`) :user:`dependabot`
#)  bases: update base executables and util module [ci skip] (:pull:`2746`) :user:`marcelotduarte`
#)  chore: use uv build and uvx (:pull:`2743`) :user:`marcelotduarte`
#)  chore: use private heap instead of stack for buffers (:pull:`2742`) :user:`marcelotduarte`
#)  fix: a segmentation fault in py313t (:pull:`2740`) :user:`marcelotduarte`
#)  tests: remove psutil to speedup tests up to 30% [ci skip] (:pull:`2741`) :user:`marcelotduarte`
#)  hooks: support opencv-python 4.10.x (including headless) (:pull:`2735`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.28.2 to 0.28.3 (:pull:`2739`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.28.1 to 0.28.2 (:pull:`2734`) :user:`dependabot`
#)  chore: use is_relative_to (py39+) to simplify code (:pull:`2732`) :user:`marcelotduarte`
#)  bases: update base executables and util module [ci skip] (:pull:`2731`) :user:`marcelotduarte`
#)  chore: cleanup (:pull:`2730`) :user:`marcelotduarte`
#)  chore: add support for Python 3.13 [macOS] (:pull:`2728`) :user:`marcelotduarte`
#)  chore: use stdlib importlib.metadata (:pull:`2727`) :user:`marcelotduarte`
#)  bases: PEP587 - Python Initialization Configuration (:pull:`2726`) :user:`marcelotduarte`
#)  chore: add support for Python 3.13 [Linux and Windows] (:pull:`2630`) :user:`marcelotduarte`
#)  doc: improve installation doc using tabs (:pull:`2725`) :user:`marcelotduarte`
#)  chore: move doc and tests requirements to directory of same name (:pull:`2724`) :user:`marcelotduarte`
#)  build(deps): update lief requirement from <0.16.0,>=0.12.0 to >=0.12.0,<0.17.0 (:pull:`2723`) :user:`dependabot`
#)  doc: improve doc for conda use and add warning to recomment its use (:pull:`2722`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2721`) :user:`pre-commit-ci`
#)  fix: support uv python in Linux (:pull:`2719`) :user:`marcelotduarte`
#)  doc: update .readthedocs.yaml [ci skip] (:pull:`2720`) :user:`marcelotduarte`
#)  hooks: fix support for Pillow in Linux (:pull:`2718`) :user:`marcelotduarte`
#)  chore: publish on testpypi on push (:pull:`2717`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.6.8 to 7.6.9 (:pull:`2716`) :user:`dependabot`
#)  chore: use python-coverage-comment-action to report coverage status (:pull:`2714`) :user:`marcelotduarte`
#)  build(deps): bump pytest from 8.3.3 to 8.3.4 (:pull:`2711`) :user:`dependabot`
#)  chore: get rid of codecov (:pull:`2712`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2710`) :user:`pre-commit-ci`
#)  build(deps): bump codecov/codecov-action from 4 to 5 (:pull:`2686`) :user:`dependabot`
#)  build-wheel: use multiple versions of a pr in testpipy (:pull:`2709`) :user:`marcelotduarte`
#)  fix: regression in module due to namespace changes (:pull:`2708`) :user:`marcelotduarte`
#)  ci: use download merge-multiple (:pull:`2707`) :user:`marcelotduarte`
#)  chore: send wheel from pr to testpypi (:pull:`2706`) :user:`marcelotduarte`
#)  chore: refactor build-wheel and ci (:pull:`2705`) :user:`marcelotduarte`
#)  ci: make rpm/deb tests do not xfail (:pull:`2700`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.6.7 to 7.6.8 (:pull:`2704`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.21.3 to 2.22.0 (:pull:`2703`) :user:`dependabot`
#)  build(deps): bump astral-sh/setup-uv from 3 to 4 (:pull:`2702`) :user:`dependabot`
#)  build-wheel: fix build sdist [ci skip] (:pull:`2699`) :user:`marcelotduarte`
#)  parser: use patchelf to get dependent file in arm [Linux] (:pull:`2695`) :user:`marcelotduarte`
#)  build-wheel: fix the build number (:pull:`2698`) :user:`marcelotduarte`
#)  pre-commit: update ruff code to new schema in validate-pyproject-schema-store 2024.11.22 (:pull:`2697`) :user:`marcelotduarte`
#)  build-wheel: fix the dev suffix (:pull:`2696`) :user:`marcelotduarte`
#)  Bump version: 7.3.0-dev0 → 7.3.0-dev.1 [ci skip] (:pull:`2694`) :user:`marcelotduarte`
#)  freezer: fix rpath [linux] (:pull:`2693`) :user:`marcelotduarte`
#)  build-wheel: Publish package to TestPyPI (:pull:`2689`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2692`) :user:`pre-commit-ci`
#)  Fix namespace package containing extensions (:pull:`2680`) :user:`sankilkis`
#)  build(deps): bump coverage from 7.6.5 to 7.6.7 (:pull:`2690`) :user:`dependabot`
#)  hooks: cleanup and reorganization (:pull:`2688`) :user:`marcelotduarte`
#)  setup: small fixes (:pull:`2687`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.6.4 to 7.6.5 (:pull:`2685`) :user:`dependabot`
#)  ci: use_oidc with codecov (:pull:`2684`) :user:`marcelotduarte`
#)  setup: copy pre-built bases on Windows (compilation is optional) (:pull:`2681`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2678`) :user:`pre-commit-ci`
#)  fix: use of build_exe --excludes with namespace packages (:pull:`2677`) :user:`marcelotduarte`
#)  fix: fix _get_top_dependencies to work on mingw (:pull:`2675`) :user:`marcelotduarte`
#)  hooks: support for pkg_resources from setuptools >= 71 (:pull:`2674`) :user:`marcelotduarte`
#)  hooks: numpy - resolve missing modules (:pull:`2670`) :user:`marcelotduarte`
#)  finder: fine-tuning the excludes list (:pull:`2669`) :user:`marcelotduarte`
#)  cli: add --verbose and --debug options (:pull:`2668`) :user:`marcelotduarte`
#)  fix: remove incorrect excludes (:pull:`2667`) :user:`marcelotduarte`
#)  fix: a more consise fix for namespace packages (:pull:`2665`) :user:`marcelotduarte`
#)  hooks: zoneinfo has an error not catched by a typo in tests (:pull:`2666`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2662`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.28.0 to 0.28.1 (:pull:`2661`) :user:`dependabot`
#)  chore: use convenient functions from stdlib that exist since 3.9 (:pull:`2658`) :user:`marcelotduarte`
#)  build(deps): bump pytest-cov from 5.0.0 to 6.0.0 (:pull:`2657`) :user:`dependabot`
#)  hooks: add fontTools (:pull:`2656`) :user:`marcelotduarte`
#)  hooks: fix for pymupdf 1.24.11+ (:pull:`2655`) :user:`marcelotduarte`
#)  cli: #2439 complementary fix on windows (:pull:`2654`) :user:`marcelotduarte`
#)  bases: update base executables and util module [ci skip] (:pull:`2652`) :user:`marcelotduarte`
#)  fix: After #2624 'Load python3.dll if it is on the target dir' (:pull:`2651`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2650`) :user:`pre-commit-ci`
#)  hooks: sets the alias for os.path (:pull:`2649`) :user:`marcelotduarte`
#)  hooks: optimize/improve more modules (:pull:`2648`) :user:`marcelotduarte`
#)  hooks: optimize/improve some modules (:pull:`2647`) :user:`marcelotduarte`
#)  chore: use uv with cibuildwheel [ci skip] (:pull:`2645`) :user:`marcelotduarte`
#)  hooks: optimize pyzmq, setuptools and pkg_resources (:pull:`2643`) :user:`marcelotduarte`
#)  finder: improve the report of missing modules (:pull:`2639`) :user:`marcelotduarte`
#)  bdist_dmg: catch errors when resource is busy (:pull:`2640`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2637`) :user:`pre-commit-ci`
#)  Enable github sponsor [ci skip] (:pull:`2638`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.6.3 to 7.6.4 (:pull:`2636`) :user:`dependabot`
#)  fix: cache only `distribution.requires` that are evaluated in the environment (:pull:`2634`) :user:`marcelotduarte`
#)  hooks: improve pyzmq (:pull:`2635`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.27.0 to 0.28.0 (:pull:`2633`) :user:`dependabot`
#)  freezer: include_msvcr now uses Redistributable files (:pull:`2451`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.6.2 to 7.6.3 (:pull:`2626`) :user:`dependabot`
#)  hooks: pydantic - #2610 missing file (:pull:`2628`) :user:`marcelotduarte`
#)  chore: simplify code using _compat and removing not required class (:pull:`2627`) :user:`marcelotduarte`
#)  freezer: Optimize the search for dependencies (:pull:`2624`) :user:`marcelotduarte`
#)  ci: migrate to astral-sh/setup-uv with cache (:pull:`2623`) :user:`marcelotduarte`
#)  tests: fix tkinter test in older macOS (:pull:`2622`) :user:`marcelotduarte`
#)  freezer: improve the use of rpath [linux] (:pull:`2621`) :user:`marcelotduarte`
#)  freezer: change the order to fix bugs with patchelf (:pull:`2620`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.6.1 to 7.6.2 (:pull:`2619`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.21.2 to 2.21.3 (:pull:`2618`) :user:`dependabot`
#)  build(deps-dev): bump pre-commit from 4.0.0 to 4.0.1 (:pull:`2617`) :user:`dependabot`
#)  build(deps): bump sphinx-tabs from 3.4.5 to 3.4.7 (:pull:`2616`) :user:`dependabot`
#)  build(deps-dev): bump blacken-docs from 1.18.0 to 1.19.0 (:pull:`2615`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2614`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pre-commit from 3.8.0 to 4.0.0 (:pull:`2613`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.26.1 to 0.27.0 (:pull:`2612`) :user:`dependabot`
#)  hooks: update pydantic hook and fix the sample (:pull:`2610`) :user:`marcelotduarte`
#)  module: preserve entry_points.txt from .egg-info (:pull:`2609`) :user:`cluck`
#)  build(deps-dev): bump cibuildwheel from 2.21.1 to 2.21.2 (:pull:`2605`) :user:`dependabot`
#)  build(deps): bump sphinx-new-tab-link from 0.6.0 to 0.6.1 (:pull:`2598`) :user:`dependabot`
#)  chore: Drop Python 3.8 (:pull:`2607`) :user:`marcelotduarte`
#)  Bump version: 7.2.3 → 7.3.0-dev0 [ci skip] (:pull:`2606`) :user:`marcelotduarte`
#)  hooks: refactor tkinter - add tests (:pull:`2604`) :user:`marcelotduarte`
#)  hooks: refactor pytz (:pull:`2603`) :user:`marcelotduarte`
#)  Bump version: 7.2.3-dev0 → 7.2.3 [ci skip] :user:`marcelotduarte`
#)  ci: remove pre-commit GHA workflow in favor of pre-commit.ci (:pull:`2602`) :user:`marcelotduarte`
#)  hooks: add urlib and fix pkg_resources (:pull:`2601`) :user:`marcelotduarte`
#)  samples: fix pycountry sample for pycountry 23+ (:pull:`2600`) :user:`marcelotduarte`
#)  hooks: support scipy 1.14 in zip library (:pull:`2597`) :user:`marcelotduarte`
#)  hooks: add VTK (vtkmodules) (:pull:`2595`) :user:`marcelotduarte`
#)  hooks: zoneinfo refactored - add tests (:pull:`2592`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2594`) :user:`pre-commit-ci`
#)  build_exe: fix include_path option (:pull:`2591`) :user:`marcelotduarte`
#)  hooks: torch - fix duplicate files (:pull:`2587`) :user:`marcelotduarte`
#)  freezer: fix reporting missing dependencies (:pull:`2590`) :user:`marcelotduarte`
#)  Bump version: 7.2.2 → 7.2.3-dev0 [ci skip] (:pull:`2589`) :user:`marcelotduarte`
#)  hooks: numpy - fix #2586 regression in windows (:pull:`2588`) :user:`marcelotduarte`
#)  hooks: numpy - fix duplicate files (:pull:`2586`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2585`) :user:`pre-commit-ci`
#)  Bump version: 7.2.1 → 7.2.2 [ci skip] (:pull:`2584`) :user:`marcelotduarte`
#)  executable: target_name does not need to be an identifier to be a valid filename (:pull:`2583`) :user:`marcelotduarte`
#)  cli: undeprecated --target-dir (:pull:`2582`) :user:`marcelotduarte`
#)  hooks: add pymupdf (:pull:`2581`) :user:`marcelotduarte`
#)  hooks: pkg_resources from setuptools >= 71 does not uses _vendor (:pull:`2580`) :user:`marcelotduarte`
#)  hooks: fix copy of files to wrong directories (qt) (:pull:`2578`) :user:`marcelotduarte`
#)  hooks: fix numpy/mkl in conda (:pull:`2579`) :user:`marcelotduarte`
#)  hooks: fix qml support for qt hooks (:pull:`2577`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.21.0 to 2.21.1 (:pull:`2573`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2571`) :user:`pre-commit-ci`
#)  build(deps): update setuptools requirement from <75,>=65.6.3 to >=65.6.3,<76 (:pull:`2569`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.26.0 to 0.26.1 (:pull:`2570`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.20.0 to 2.21.0 (:pull:`2567`) :user:`dependabot`
#)  bases: update base executables and util module [ci skip] (:pull:`2566`) :user:`marcelotduarte`
#)  Bump version: 7.2.0 → 7.2.1 [ci skip] (:pull:`2565`) :user:`marcelotduarte`
#)  build(deps): bump pytest from 8.3.2 to 8.3.3 (:pull:`2562`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2561`) :user:`pre-commit-ci`
#)  hooks: add tortoise-orm (:pull:`2564`) :user:`marcelotduarte`
#)  hooks: fix regression in qt windows (:pull:`2563`) :user:`marcelotduarte`
#)  build(deps): bump sphinx-new-tab-link from 0.5.3 to 0.6.0 (:pull:`2558`) :user:`dependabot`
#)  build(deps): update setuptools requirement (:pull:`2556`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2550`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.25.1 to 0.26.0 (:pull:`2549`) :user:`dependabot`
#)  build(deps): bump sphinx-new-tab-link from 0.5.2 to 0.5.3 (:pull:`2547`) :user:`dependabot`
#)  ci: run pytest on build wheels (instead of editable wheels) (:pull:`2555`) :user:`marcelotduarte`
#)  setup: do not copy libraries in develop mode (:pull:`2543`) :user:`marcelotduarte`
#)  docs: use brackets for the default value of option arguments (:pull:`2541`) :user:`marcelotduarte`
#)  build(deps,docs): update python dependencies (:pull:`2540`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.25.0 to 0.25.1 (:pull:`2538`) :user:`dependabot`
#)  build(deps): use setuptools >= 70.1 to build (get rid of wheel) (:pull:`2539`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.24.3 to 0.25.0 (:pull:`2537`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2536`) :user:`pre-commit-ci`
#)  build(deps-dev): bump cibuildwheel from 2.19.2 to 2.20.0 (:pull:`2535`) :user:`dependabot`
#)  build(deps): bump coverage from 7.6.0 to 7.6.1 (:pull:`2533`) :user:`dependabot`
#)  bases: fix regression because the order used by clang-format (:pull:`2530`) :user:`marcelotduarte`
#)  bdist_rpm: fix use of 'cxfreeze bdist_rpm' command (:pull:`2529`) :user:`marcelotduarte`
#)  build(deps): bump sphinx-new-tab-link from 0.5.1 to 0.5.2 (:pull:`2528`) :user:`dependabot`
#)  pre-commit: use clang-format (:pull:`2525`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2524`) :user:`pre-commit-ci`
#)  build(deps): update setuptools requirement from <72,>=65.6.3 to >=65.6.3,<73 (:pull:`2523`) :user:`dependabot`
#)  build(deps): bump sphinx-new-tab-link from 0.5.0 to 0.5.1 (:pull:`2522`) :user:`dependabot`
#)  build(deps): prepare for setuptools stop vendoring packages (:pull:`2521`) :user:`marcelotduarte`
#)  build(deps): bump pytest from 8.3.1 to 8.3.2 (:pull:`2520`) :user:`dependabot`
#)  parser: add compatibility with lief 0.15.x (:pull:`2519`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2517`) :user:`pre-commit-ci`
#)  build(deps): bump pytest from 8.2.2 to 8.3.1 (:pull:`2516`) :user:`dependabot`
#)  build_exe: MingW and posix systems silently ignore include_msvcr option (:pull:`2514`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.24.2 to 0.24.3 (:pull:`2511`) :user:`dependabot`
#)  build(deps): update setuptools requirement from <71,>=65.6.3 to >=65.6.3,<72 (:pull:`2512`) :user:`dependabot`
