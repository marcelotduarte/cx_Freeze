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


Version 8.5 (Nov 24)
--------------------

#)  Bump version: 8.5.0-dev.0 → 8.5.0 [ci skip] (:pr:`3180`) :user:`marcelotduarte`
#)  chore: prepare changelog and release notes (:pr:`3179`) :user:`marcelotduarte`
#)  ci: revert actions/checkout - breaks coverage comment (:pr:`3178`) :user:`marcelotduarte`
#)  build(deps): bump astral-sh/setup-uv from 7.1.3 to 7.1.4 (:pr:`3177`) :user:`dependabot`
#)  ci: add permission and ignore bot branches (:pr:`3176`) :user:`marcelotduarte`
#)  ci: fix content permissions (:pr:`3175`) :user:`marcelotduarte`
#)  ci: revert security change that block coverage comment (:pr:`3174`) :user:`marcelotduarte`
#)  bdist_msi: fix target_name usage and revert some old patches (:pr:`3173`) :user:`marcelotduarte`
#)  build(deps): bump actions/checkout from 5.0.1 to 6.0.0 (:pr:`3172`) :user:`dependabot`
#)  bdist_appimage: add `updateinformation` option (:pr:`3166`) :user:`marcelotduarte`
#)  build(deps): bump github/codeql-action from 3.31.3 to 4.31.4 (:pr:`3171`) :user:`dependabot`
#)  build(deps): bump py-cov-action/python-coverage-comment-action from 6494290850a5098c2836298dad8f11082b4ceaa9 to 39ffc771120970de615612f01a030260bcb45443 (:pr:`3169`) :user:`dependabot`
#)  build(deps): bump actions/checkout from 5.0.0 to 5.0.1 (:pr:`3168`) :user:`dependabot`
#)  build(deps): bump coverage from 7.11.3 to 7.12.0 (:pr:`3170`) :user:`dependabot`
#)  Documentation tweaks in preparation for version release [ci skip] (:pr:`3167`) :user:`marcelotduarte`
#)  [StepSecurity] Apply security best practices (:pr:`3165`) :user:`bot`
#)  [StepSecurity] ci: Harden GitHub Actions (:pr:`3164`) :user:`bot`
#)  tests: make tests pass on mingw and conda [ci skip] (:pr:`3162`) :user:`marcelotduarte`
#)  chore: minor revision of project configuration (:pr:`3161`) :user:`marcelotduarte`
#)  build(deps): bump pytest from 9.0.0 to 9.0.1 (:pr:`3160`) :user:`dependabot`
#)  bdist_msi: fix initial_target_dir on Windows ARM64-based machines (:pr:`3140`) :user:`marcelotduarte`
#)  feat(hooks): add winrt module hook for automatic package inclusion (:pr:`3151`) :user:`amnweb`
#)  hooks: update set of excludes/ignores names (:pr:`3158`) :user:`marcelotduarte`
#)  bdist_appimage: make entrypoint script POSIX-compliant (:pr:`3157`) :user:`marcelotduarte`
#)  hooks: add backports.zstd (:pr:`3156`) :user:`marcelotduarte`
#)  build(deps-dev): bump pre-commit from 4.3.0 to 4.4.0 (:pr:`3155`) :user:`dependabot`
#)  build(deps): bump pytest from 8.4.2 to 9.0.0 (:pr:`3154`) :user:`dependabot`
#)  build(deps): bump coverage from 7.11.1 to 7.11.3 (:pr:`3153`) :user:`dependabot`
#)  chore: change warning about conda usage [ci skip] (:pr:`3152`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.11.0 to 7.11.1 (:pr:`3150`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`3149`) :user:`pre-commit-ci`
#)  tests: simplify build_exe tests (:pr:`3148`) :user:`marcelotduarte`
#)  finder: optimized implementation of '_find_editable_spec' (:pr:`3147`) :user:`egor.martiniuc`
#)  build(deps): bump actions/upload-artifact from 4 to 5 (:pr:`3145`) :user:`dependabot`
#)  build(deps): bump actions/download-artifact from 5 to 6 (:pr:`3144`) :user:`dependabot`
#)  build(deps): update lief requirement from <=0.16.6,>=0.15.1 to >=0.15.1,<=0.17.1 (:pr:`3141`) :user:`marcelotduarte`
#)  tests: fix tests on arm64 (:pr:`3142`) :user:`marcelotduarte`
#)  bdist_appimage: add `sign` and `sign-key` options (:pr:`3138`) :user:`marcelotduarte`
#)  chore: small review of the documentation [ci skip] (:pr:`3137`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.10.7 to 7.11.0 (:pr:`3136`) :user:`dependabot`
#)  chore: drop Python 3.9 support (:pr:`3135`) :user:`marcelotduarte`
#)  bdist_appimage: minor revision and fixes (:pr:`3134`) :user:`marcelotduarte`
#)  bdist_appimage: add support for 'gui' app in desktop file (:pr:`3133`) :user:`marcelotduarte`
#)  chore: refactor more code related to bytecode and executable (:pr:`3132`) :user:`marcelotduarte`
#)  bdist_appimage: replace appimagekit option with appimagetool option (:pr:`3131`) :user:`marcelotduarte`
#)  bdist_appimage: add "runtime-file" argument to bdist_appimage command (:pr:`3063`) :user:`mail`
#)  chore: add support for Python 3.14 (:pr:`3130`) :user:`marcelotduarte`
#)  chore: bump ruff from 0.13.3 to 0.14.0 and tweak some options (:pr:`3129`) :user:`marcelotduarte`
#)  tests: update supported versions of packages used in tests (:pr:`3128`) :user:`marcelotduarte`
#)  chore: refactor finder scan code (:pr:`3126`) :user:`marcelotduarte`
#)  build(deps): bump astral-sh/setup-uv from 6 to 7 (:pr:`3123`) :user:`dependabot`
#)  chore: minor tweaks in internal imports (:pr:`3122`) :user:`marcelotduarte`
#)  build(deps): bump github/codeql-action from 3 to 4 (:pr:`3121`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 1.2.3 to 1.2.4 (:pr:`3120`) :user:`dependabot`
#)  build(deps): bump python-msilib to 0.2.0 (:pr:`3118`) :user:`marcelotduarte`
#)  build(deps): bump setuptools to 78.1.1 to fix path traversal vulnerability in PackageIndex.download (:pr:`3117`) :user:`marcelotduarte`
#)  chore: python-msilib as dependency for python 3.13 [windows] (:pr:`3115`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`3114`) :user:`pre-commit-ci`
#)  doc: add freeze-core to the docs and cleanup [ci skip] (:pr:`3113`) :user:`marcelotduarte`
#)  chore: bump freeze-core to 0.2.0 (:pr:`3112`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.10.6 to 7.10.7 (:pr:`3111`) :user:`dependabot`
#)  chore: freeze-core as dependency (:pr:`3109`) :user:`marcelotduarte`
#)  Bump version: 8.4.1 → 8.5.0-dev.0 [ci skip] (:pr:`3108`) :user:`marcelotduarte`
#)  Bump version: 8.4.0 → 8.4.1 [ci skip] (:pr:`3107`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 1.2.2 to 1.2.3 (:pr:`3106`) :user:`dependabot`
#)  tests: avoid duplicate qt libs (:pr:`3068`) :user:`frmdstryr`
#)  tests: use include_msvcr in tests to pass in a clean system (:pr:`3105`) :user:`marcelotduarte`
#)  tests: fix tests on msys2 [ci skip] (:pr:`3104`) :user:`marcelotduarte`
#)  build(deps-dev): workaround for bump-my-version (:pr:`3103`) :user:`marcelotduarte`
#)  build(deps): bump pytest-mock from 3.15.0 to 3.15.1 (:pr:`3101`) :user:`dependabot`
#)   build(deps): update lief requirement from <=0.16.6,>=0.15.1 to >=0.15.1,<=0.17.0 (:pr:`3100`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 1.2.1 to 1.2.2 (:pr:`3099`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`3097`) :user:`marcelotduarte`
#)  Fix Windows permission error (:pr:`3095`) :user:`timlassiter11`
#)  build(deps): bump pytest-mock from 3.14.1 to 3.15.0 (:pr:`3094`) :user:`dependabot`
#)  build(deps): bump pytest from 8.4.1 to 8.4.2 (:pr:`3093`) :user:`dependabot`
#)  build(deps): bump actions/setup-python from 5 to 6 (:pr:`3092`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`3091`) :user:`pre-commit-ci`
#)  build(deps): bump coverage from 7.10.5 to 7.10.6 (:pr:`3089`) :user:`dependabot`
#)  hooks: improve lazy loader support for skimage (:pr:`3087`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.10.4 to 7.10.5 (:pr:`3088`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`3086`) :user:`pre-commit-ci`
#)  freezer: ignore .pyi, .pxd, .pyx, etc while copy package data (:pr:`3084`) :user:`marcelotduarte`
#)  hooks: pytz - ignore warning at runtime (:pr:`3083`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.10.3 to 7.10.4 (:pr:`3080`) :user:`dependabot`
#)  tests: fix venv tests in mingw and conda [ci skip] (:pr:`3081`) :user:`marcelotduarte`
#)  fix: regression in qt hooks (introduced in #2788) - since 7.2.9 (:pr:`3079`) :user:`marcelotduarte`
#)  tests: run frozen executables outside of a venv (:pr:`3076`) :user:`marcelotduarte`
#)  fix: --include-path should consider existing .pth files (:pr:`3077`) :user:`marcelotduarte`
#)  tests: pyproj 3.7.2 supports py3.13t and windows arm64 (:pr:`3075`) :user:`marcelotduarte`
#)  tests: improve zoneinfo/tzdata tests (:pr:`3073`) :user:`marcelotduarte`
#)  build(deps): bump actions/checkout from 4 to 5 (:pr:`3072`) :user:`dependabot`
#)  build(deps-dev): bump pre-commit from 4.2.0 to 4.3.0 (:pr:`3070`) :user:`dependabot`
#)  build(deps): bump coverage from 7.10.2 to 7.10.3 (:pr:`3069`) :user:`marcelotduarte`

Version 8.4 (Aug 11)
--------------------
#)  Bump version: 8.4.0-dev.0 → 8.4.0 [ci skip] (:pr:`3066`) :user:`marcelotduarte`
#)  chore: replace pytest-cov with pure coverage with patch subprocess support (:pr:`3065`) :user:`marcelotduarte`
#)  build(deps): bump actions/download-artifact from 4 to 5 (:pr:`3062`) :user:`dependabot`
#)  build(deps): bump coverage from 7.10.1 to 7.10.2 (:pr:`3061`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`3060`) :user:`pre-commit-ci`
#)  build(deps): bump coverage from 7.9.2 to 7.10.1 (:pr:`3057`) :user:`dependabot`
#)  tests: improve venv tests and add support for pip installer (:pr:`3059`) :user:`marcelotduarte`
#)  hooks: fix numpy+mkl on conda [ci skip] (:pr:`3058`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`3056`) :user:`pre-commit-ci`
#)  hooks: fix pyav on conda windows [ci skip] (:pr:`3054`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 1.2.0 to 1.2.1 (:pr:`3053`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`3052`) :user:`pre-commit-ci`
#)  tests: make ortools tests pass on conda (:pr:`3051`) :user:`marcelotduarte`
#)  chore: improve dev tools (:pr:`3050`) :user:`marcelotduarte`
#)  module: fix support for dylibs [macos] (:pr:`3046`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`3044`) :user:`pre-commit-ci`
#)  hooks: support scikit-learn 1.7, optimization, add test (:pr:`3043`) :user:`marcelotduarte`
#)  hooks: optimize scipy (partially) (:pr:`3042`) :user:`marcelotduarte`
#)  chore: use sphinx-issues (:pr:`3041`) :user:`marcelotduarte`
#)  fix: use the latest manylinux image to fix sqlite3 issue on linux (:pr:`3040`) :user:`marcelotduarte`
#)  finder: detect editable packages (Python 3.10+ only) (:pr:`3036`) :user:`frmdstryr`
#)  tests: improve conftest to better capture stderr (:pr:`3039`) :user:`marcelotduarte`
#)  tests: improvements using pytest.RunResult (:pr:`3037`) :user:`marcelotduarte`
#)  hooks: more optimization to numpy hooks, separated test for mkl (:pr:`3035`) :user:`marcelotduarte`
#)  hooks: update pyproj, add test (:pr:`3034`) :user:`marcelotduarte`
#)  chore: tweak docstring [ci skip] (:pr:`3033`) :user:`marcelotduarte`
#)  hooks: optimize pyzmq, add test (:pr:`3032`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.9.1 to 7.9.2 (:pr:`3031`) :user:`dependabot`
#)  build(deps): bump pytest-xdist from 3.7.0 to 3.8.0 (:pr:`3030`) :user:`dependabot`
#)  module: cleanup (:pr:`3029`) :user:`marcelotduarte`
#)  hooks: convert qt hooks to use ModuleHook (:pr:`3028`) :user:`marcelotduarte`
#)  fix: build sdist and wheel issues (:pr:`3027`) :user:`marcelotduarte`
#)  hooks: convert a bunch of hooks to use ModuleHook - part 2 (:pr:`3026`) :user:`marcelotduarte`
#)  tests: add test for PR 2998 (:pr:`3025`) :user:`marcelotduarte`
#)  startup: Fixed crash when sys.path contains non-str type (:pr:`2998`) :user:`1ZUMIKun`
#)  hooks: convert a bunch of hooks to use ModuleHook (:pr:`3024`) :user:`marcelotduarte`
#)  bases: update base executables and util module [ci skip] (:pr:`3023`) :user:`marcelotduarte`
#)  hooks: optimize pandas (partially) (:pr:`3022`) :user:`marcelotduarte`
#)  hooks: optimize matplotlib, fonttools, pyparsing and others (:pr:`3021`) :user:`marcelotduarte`
#)  hooks: update global_names for some modules, especially numpy (:pr:`3020`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`3019`) :user:`pre-commit-ci`
#)  hooks: support for scipy 1.16 (:pr:`3018`) :user:`marcelotduarte`
#)  tests: small revision [ci skip] (:pr:`3017`) :user:`marcelotduarte`
#)  tests: tweak grammar [ci skip] (:pr:`3016`) :user:`marcelotduarte`
#)  tests: improve conftest - add install_dependencies (:pr:`3015`) :user:`marcelotduarte`
#)  tests: sets a longer timeout for slower tests in conda [ci skip] (:pr:`3014`) :user:`marcelotduarte`
#)  hooks: update stub for qt [ci skip] (:pr:`3013`) :user:`marcelotduarte`
#)  tests: enable a minimal test for multiprocess hook (:pr:`3011`) :user:`marcelotduarte`
#)  hooks: multiprocessing and multiprocess refactored (:pr:`3010`) :user:`marcelotduarte`
#)  hooks: multiprocessing - fix Python 3.13.4+ bug introduced by gh-80334 on Windows (:pr:`3009`) :user:`marcelotduarte`
#)  bases: update base executables and util module [ci skip] (:pr:`3008`) :user:`marcelotduarte`
#)  chore: fix ruff D104, E501 (partial) [ci skip] (:pr:`3007`) :user:`marcelotduarte`
#)  build(deps): bump pytest from 8.4.0 to 8.4.1 (:pr:`3006`) :user:`dependabot`
#)  tests: reduce fixture setup phase and reduce disk usage (:pr:`3005`) :user:`marcelotduarte`
#)  build(deps): bump ruff to 0.12.0 and revision of rules [ci skip] (:pr:`3004`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.9.0 to 7.9.1 (:pr:`3003`) :user:`dependabot`
#)  build(deps): bump pytest-cov from 6.1.1 to 6.2.1 (:pr:`3002`) :user:`dependabot`
#)  build(deps): bump coverage from 7.8.2 to 7.9.0 (:pr:`3001`) :user:`dependabot`
#)  build(deps): update patchelf requirements to >=0.14,<0.18 [ci skip] (:pr:`3000`) :user:`marcelotduarte`
#)  tests: implement a venv to tests hooks (:pr:`2997`) :user:`marcelotduarte`
#)  build-wheel: fix regression [ci skip] (:pr:`2999`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 1.1.4 to 1.2.0 (:pr:`2996`) :user:`dependabot`
#)  tests: disable slow tests on conda-forge [ci skip] (:pr:`2994`) :user:`marcelotduarte`
#)  tests: fix tests using lief and pymupdf on conda-forge [ci skip] (:pr:`2993`) :user:`marcelotduarte`
#)  chore: string format (cosmetic) [ci skip] (:pr:`2992`) :user:`marcelotduarte`
#)  chore: use shellcheck (:pr:`2991`) :user:`marcelotduarte`
#)  chore: use prettier [ci skip] (:pr:`2990`) :user:`marcelotduarte`
#)  tests: fix test on conda windows and use libmanba-solver [ci skip] (:pr:`2989`) :user:`marcelotduarte`
#)  chore: add support to install tools/requirements on conda (:pr:`2988`) :user:`marcelotduarte`
#)  tests: add support to test on conda build [ci skip] (:pr:`2987`) :user:`marcelotduarte`
#)  hooks: fix pymupdf to work in conda [ci skip] (:pr:`2986`) :user:`marcelotduarte`
#)  sources: upgrade pythoncapi_compat.h [ci skip] (:pr:`2985`) :user:`marcelotduarte`
#)  build(deps): bump pytest from 8.3.5 to 8.4.0 (:pr:`2984`) :user:`dependabot`
#)  tests: pymupdf is broken in mingw [ci skip] (:pr:`2983`) :user:`marcelotduarte`
#)  tests: pymupdf not supported in mingw [ci skip] (:pr:`2982`) :user:`marcelotduarte`
#)  build(deps): update lief requirement from <=0.16.5,>=0.15.1 to >=0.15.1,<=0.16.6 (:pr:`2981`) :user:`marcelotduarte`
#)  build(deps): bump pytest-xdist from 3.6.1 to 3.7.0 (:pr:`2979`) :user:`dependabot`
#)  build(deps): update setuptools requirement from <=80.8.0,>=65.6.3 to >=65.6.3,<=80.9.0 (:pr:`2978`) :user:`dependabot`
#)  hooks: fix pymupdf - add tests (:pr:`2977`) :user:`marcelotduarte`
#)  freezer: Fix errors with invalid file dates in zipfile (:pr:`2975`) :user:`DamitusThyYeetus123`
#)  hooks: after #2962, adjust pyside2 and pyside6 (:pr:`2976`) :user:`marcelotduarte`
#)  build(deps): bump pytest-mock from 3.14.0 to 3.14.1 (:pr:`2974`) :user:`dependabot`
#)  bases: update base executables and util module [ci skip] (:pr:`2973`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.8.1 to 7.8.2 (:pr:`2972`) :user:`dependabot`
#)  chore: update pythoncapi_compat (:pr:`2971`) :user:`marcelotduarte`
#)  module: A rewrite of how dynamic libraries distributed with a package are frozen (:pr:`2962`) :user:`marcelotduarte`
#)  tests: add matplotlib (:pr:`2969`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 1.1.3 to 1.1.4 (:pr:`2968`) :user:`dependabot`
#)  build(deps): bump coverage from 7.8.0 to 7.8.1 (:pr:`2967`) :user:`dependabot`
#)  build(deps): update setuptools requirement from <=80.7.1,>=65.6.3 to >=65.6.3,<=80.8.0 (:pr:`2966`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2965`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 1.1.2 to 1.1.3 (:pr:`2964`) :user:`dependabot`
#)  hooks: fix shapely in linux - add tests (:pr:`2963`) :user:`marcelotduarte`
#)  bdist_mac: Update include_frameworks copy to preserve symlinks (:pr:`2959`) :user:`exiva`
#)  build(deps): update setuptools requirement from <=80.4.0,>=65.6.3 to >=65.6.3,<=80.7.1 (:pr:`2960`) :user:`dependabot`
#)  build(deps): bump pluggy from 1.5.0 to 1.6.0 (:pr:`2961`) :user:`dependabot`
#)  tests: add one more test for dep_parser module (:pr:`2958`) :user:`marcelotduarte`
#)  test: module.DistributionCache test conversion of egg_info to dist_info (:pr:`2957`) :user:`marcelotduarte`
#)  tests: skip msvcr tests in mingw and macos [ci skip] (:pr:`2956`) :user:`marcelotduarte`
#)  tests: add winmsvcr_repack tests (:pr:`2955`) :user:`marcelotduarte`

Version 8.3 (May 11)
--------------------
#)  Bump version: 8.3.0-dev.0 → 8.3.0 [ci skip] (:pr:`2953`) :user:`marcelotduarte`
#)  chore: build wheels only for Python 3.11-3.13 on non conventional archs [ci skip] (:pr:`2952`) :user:`marcelotduarte`
#)  tests: improve install-tools and fixes build-wheel (:pr:`2950`) :user:`marcelotduarte`
#)  tests: improve build and test on mingw (:pr:`2947`) :user:`marcelotduarte`
#)  tests: use include_msvcr because tests should pass in a clean system (:pr:`2949`) :user:`marcelotduarte`
#)  tests: tweaks to work on mingw (:pr:`2948`) :user:`marcelotduarte`
#)  build(deps): bump pytest-timeout from 2.3.1 to 2.4.0 (:pr:`2946`) :user:`dependabot`
#)  build(deps): update setuptools requirement from <=80.3.0,>=65.6.3 to >=65.6.3,<=80.3.1 (:pr:`2945`) :user:`dependabot`
#)  build(deps): update lief requirement to >= 0.15.1 [windows] (:pr:`2944`) :user:`marcelotduarte`
#)  chore: experimental support for windows arm64 (:pr:`2943`) :user:`marcelotduarte`
#)  hooks: ensure zlib1.dll is copied if lief is not used in Python 3.12+ (:pr:`2942`) :user:`marcelotduarte`
#)  build(deps): update setuptools requirement from <=80.0.0,>=65.6.3 to >=65.6.3,<=80.1.0 (:pr:`2941`) :user:`dependabot`
#)  hooks: add zeroconf (:pr:`2932`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.23.2 to 2.23.3 (:pr:`2939`) :user:`dependabot`
#)  build(deps): update setuptools requirement from <=79.0.1,>=65.6.3 to >=65.6.3,<=80.0.0 (:pr:`2940`) :user:`dependabot`
#)  bases: update base executables and util module [ci skip] (:pr:`2937`) :user:`marcelotduarte`
#)  hooks: typo in sklearn hook (:pr:`2930`) :user:`marcelotduarte`
#)  chore: use codespell (:pr:`2936`) :user:`marcelotduarte`
#)  hooks: support pyarrow 20 on windows (:pr:`2935`) :user:`marcelotduarte`
#)  chore: get rid of typing_extensions (:pr:`2934`) :user:`marcelotduarte`
#)  tests: improve fixture tmp_package (install binary) (:pr:`2933`) :user:`marcelotduarte`
#)  compat: normalize SOABI in mingw python (:pr:`2931`) :user:`marcelotduarte`
#)  build(deps): bump astral-sh/setup-uv from 5 to 6 (:pr:`2928`) :user:`dependabot`
#)  build(deps): update setuptools requirement from <=79.0.0,>=65.6.3 to >=65.6.3,<=79.0.1 (:pr:`2927`) :user:`dependabot`
#)  tests: improve dep_parser tests (:pr:`2925`) :user:`marcelotduarte`
#)  tests: improve bdist_appimage (:pr:`2924`) :user:`marcelotduarte`
#)  Bump version: 8.2.0 → 8.3.0-dev.0 [ci skip] (:pr:`2923`) :user:`marcelotduarte`

Version 8.2 (Apr 22)
--------------------
#)  Bump version: 8.1.0 → 8.2.0 [ci skip] (:pr:`2922`) :user:`marcelotduarte`
#)  ci: configure coverage paths (:pr:`2921`) :user:`marcelotduarte`
#)  tests: fix pytest-cov issue (:pr:`2919`) :user:`marcelotduarte`
#)  tests: use GHA Python 3.13t and small changes (:pr:`2920`) :user:`marcelotduarte`
#)  tests: improve some tests for better coverage (:pr:`2918`) :user:`marcelotduarte`
#)  build(deps): update setuptools requirement from <=78.1.0,>=65.6.3 to >=65.6.3,<=79.0.0 (:pr:`2916`) :user:`dependabot`
#)  dep_parser: minor fix to improve tests (:pr:`2915`) :user:`marcelotduarte`
#)  tests: fix dep_parser test in windows (:pr:`2914`) :user:`marcelotduarte`
#)  tests: improve dep_parser test (:pr:`2913`) :user:`marcelotduarte`
#)  tests: add anyio, asyncio, uvloop (:pr:`2912`) :user:`marcelotduarte`
#)  tests: add pyarrow, bcrypt<4 (:pr:`2911`) :user:`marcelotduarte`
#)  module: improve use of constansts, add tests (:pr:`2909`) :user:`marcelotduarte`
#)  hooks: fix scipy[zip] in Python>=3.10 [macos] (:pr:`2908`) :user:`marcelotduarte`
#)  hooks: fix mkl on zip and fix tests (:pr:`2907`) :user:`marcelotduarte`
#)  tests: test ConstantsModule / BUILD_CONSTANTS (:pr:`2906`) :user:`marcelotduarte`
#)  tests: add more tests for hooks of crypto packages (:pr:`2905`) :user:`marcelotduarte`
#)  tests: improve coverage of Executable class (:pr:`2904`) :user:`marcelotduarte`
#)  build(deps-doc): bump sphinx to 8.2.3 [ci skip] (:pr:`2903`) :user:`marcelotduarte`
#)  tests: improve winversioninfo tests (:pr:`2901`) :user:`marcelotduarte`
#)  tests: improve tmp_package fixture adding cwd (:pr:`2902`) :user:`marcelotduarte`
#)  tests: add test for rasterio (test DistributionCache.binary_files) (:pr:`2900`) :user:`marcelotduarte`
#)  tests: improve coverage a bit (:pr:`2899`) :user:`marcelotduarte`
#)  tests: add tests to hooks of pytz and ctypes (:pr:`2893`) :user:`marcelotduarte`
#)  cli: fix case comparison in windows (:pr:`2898`) :user:`marcelotduarte`
#)  module: add 'name' property to DistributionCache (:pr:`2897`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2896`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 1.1.1 to 1.1.2 (:pr:`2895`) :user:`dependabot`
#)  tests: improve tests on windows (:pr:`2892`) :user:`marcelotduarte`
#)  tests: improve hooks tests with a function to install a package (:pr:`2891`) :user:`marcelotduarte`
#)  ci: Fetch only the required files for testing (:pr:`2890`) :user:`marcelotduarte`
#)  tests: improve conftest (:pr:`2889`) :user:`marcelotduarte`
#)  tests: add scipy sample as a hook test (:pr:`2888`) :user:`marcelotduarte`
#)  tests: cleanup (:pr:`2887`) :user:`marcelotduarte`
#)  tests: port more tests to use the new fixture 4 (:pr:`2886`) :user:`marcelotduarte`
#)  tests: port more tests to use the new fixture 3 (:pr:`2885`) :user:`marcelotduarte`
#)  tests: port more tests to use the new fixture 2 (:pr:`2884`) :user:`marcelotduarte`
#)  tests: improve mp tests (:pr:`2882`) :user:`marcelotduarte`
#)  tests: port more tests to use the new fixture (:pr:`2883`) :user:`marcelotduarte`
#)  tests: add conftest and port stdlib hooks test to use it (:pr:`2881`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2880`) :user:`pre-commit-ci`
#)  build(deps): bump pytest-cov from 6.1.0 to 6.1.1 (:pr:`2879`) :user:`dependabot`
#)  hooks: fix scipy hook on mingw and catch similar errors (:pr:`2877`) :user:`marcelotduarte`
#)  doc: small review [ci skip] (:pr:`2876`) :user:`marcelotduarte`
#)  chore: use sys.prefix as frozen directory (:pr:`2874`) :user:`marcelotduarte`
#)  chore: support for PEP 639 (:pr:`2873`) :user:`marcelotduarte`
#)  chore: use importlib.resources (:pr:`2872`) :user:`marcelotduarte`
#)  bdist_msi: Make MSI checkbox to "launch after install" optional (:pr:`2871`) :user:`jeroen`

Version 8.1 (Apr 02)
--------------------

#)  Bump version: 8.0.0 → 8.1.0 [ci skip] (:pr:`2868`) :user:`marcelotduarte`
#)  chore: support for setuptools fix for pep491 (:pr:`2867`) :user:`marcelotduarte`
#)  build(deps): bump pytest-cov from 6.0.0 to 6.1.0 (:pr:`2866`) :user:`dependabot`
#)  build(deps): bump sphinx-new-tab-link from 0.7.0 to 0.8.0 (:pr:`2865`) :user:`dependabot`
#)  hooks: fix scipy (using numpy) (:pr:`2862`) :user:`marcelotduarte`
#)  bdist_msi: Add a launch on finish checkbox to the MSI installer (:pr:`2854`) :user:`MeGaGiGaGon`
#)  build(deps): bump coverage from 7.7.1 to 7.8.0 (:pr:`2864`) :user:`dependabot`
#)  hooks: include source files that uses @torch.jit._overload_method (:pr:`2863`) :user:`marcelotduarte`
#)  fix: ruff A005 (:pr:`2859`) :user:`marcelotduarte`
#)  hooks: zlib module requires the zlib.dll to be present in the executable directory [conda/Windows] (:pr:`2855`) :user:`marcelotduarte`
#)  hooks: add argon2-cffi (:pr:`2857`) :user:`marcelotduarte`
#)  fix: ruff LOG015 [ci skip] (:pr:`2858`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.23.1 to 2.23.2 (:pr:`2853`) :user:`dependabot`
#)  hooks: update to support pymupdf 1.25.4 (:pr:`2851`) :user:`marcelotduarte`
#)  hooks: fix importlib hook (:pr:`2852`) :user:`marcelotduarte`
#)  hooks: enable asynchat and asyncore usage via pyasynchat and pyasyncore packages (:pr:`2850`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2849`) :user:`pre-commit-ci`
#)  doc: fix version documentation [ci skip] (:pr:`2847`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 1.0.2 to 1.1.1 (:pr:`2846`) :user:`dependabot`
#)  Update setup_script.rst fixed typo in docs (:pr:`2845`) :user:`philipp`
#)  build(deps): bump coverage from 7.7.0 to 7.7.1 (:pr:`2840`) :user:`dependabot`
#)  fix: use only console based on PEP587 on Python 3.13 (:pr:`2842`) :user:`marcelotduarte`

Version 8.0 (Mar 21)
--------------------

#)  hooks: add timm package (:pr:`2834`) :user:`marcelotduarte`
#)  build(deps-dev): bump pre-commit from 4.1.0 to 4.2.0 (:pr:`2833`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2832`) :user:`pre-commit-ci`
#)  build(deps): bump coverage from 7.6.12 to 7.7.0 (:pr:`2830`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.23.0 to 2.23.1 (:pr:`2831`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2828`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 1.0.1 to 1.0.2 (:pr:`2827`) :user:`dependabot`
#)  build(deps): bump sphinx-new-tab-link from 0.6.1 to 0.7.0 (:pr:`2826`) :user:`dependabot`
#)  build(deps): bump pytest from 8.3.4 to 8.3.5 (:pr:`2818`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.32.1 to 1.0.1 (:pr:`2824`) :user:`dependabot`
#)  build(deps): update lief requirement from <=0.16.3,>=0.13.2 to >=0.13.2,<=0.16.4 (:pr:`2816`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.22.0 to 2.23.0 (:pr:`2819`) :user:`dependabot`
#)  fix: setuptools 75.8.1 breaks auditwheel (:pr:`2823`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2814`) :user:`pre-commit-ci`
#)  build(deps): update myst-parser requirement from <=4.0.0,>=3.0.1 to >=3.0.1,<=4.0.1 (:pr:`2809`) :user:`dependabot`
#)  build(deps): bump coverage from 7.6.11 to 7.6.12 (:pr:`2806`) :user:`dependabot`
#)  build-wheel: use ubuntu 22.04 emulator to build ppc64le (:pr:`2805`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2804`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.32.0 to 0.32.1 (:pr:`2803`) :user:`dependabot`
#)  build(deps): bump coverage from 7.6.10 to 7.6.11 (:pr:`2802`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.31.1 to 0.32.0 (:pr:`2800`) :user:`dependabot`
#)  fix: missing dlls in top directory [mingw] (:pr:`2799`) :user:`marcelotduarte`
#)  hooks: fix shapely [windows] (:pr:`2797`) :user:`marcelotduarte`
#)  build(deps): update lief requirement from <=0.16.2,>=0.13.2 to >=0.13.2,<=0.16.3 (:pr:`2795`) :user:`dependabot`
#)  tests: fix msi test (:pr:`2796`) :user:`marcelotduarte`
#)  doc: fix typo [ci skip] (:pr:`2793`) :user:`marcelotduarte`
#)  doc: improve documentation on using pyproject.toml [ci skip] (:pr:`2792`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.29.0 to 0.31.1 (:pr:`2790`) :user:`dependabot`
#)  hooks: ctypes, ssl, sqlite3 - conda-forge (:pr:`2791`) :user:`marcelotduarte`
#)  chore: support ruff 0.9.x (:pr:`2789`) :user:`marcelotduarte`
#)  hooks: copy only shared libs of Qt in qt hooks (:pr:`2788`) :user:`marcelotduarte`
#)  hooks: pytorch 2.6.0 (:pr:`2787`) :user:`marcelotduarte`
#)  chore: build_wheel improvements and use of ubuntu-24.04-arm runner (:pr:`2784`) :user:`marcelotduarte`
#)  hooks: complementary fix for pytorch/nvidia/torchmetrics (:pr:`2782`) :user:`marcelotduarte`
#)  hooks: fix pytorch on macOS (:pr:`2781`) :user:`marcelotduarte`
#)  build(deps-dev): bump pre-commit from 4.0.1 to 4.1.0 (:pr:`2778`) :user:`dependabot`
#)  fix: work with lief disabled or uninstalled (:pr:`2777`) :user:`marcelotduarte`
#)  appimage: use full path of appimagetool (:pr:`2771`) :user:`marcelotduarte`
#)  chore: lief>=0.13.2,<=0.16.2 [windows] (:pr:`2770`) :user:`marcelotduarte`
#)  chore: use new features of uv (:pr:`2769`) :user:`marcelotduarte`
#)  chore: enable experimental free-threaded python 3.13 on unix (:pr:`2759`) :user:`marcelotduarte`
#)  ci: minor tweaks and fixes (:pr:`2768`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2766`) :user:`pre-commit-ci`
#)  ci: fix some build and test issues (:pr:`2767`) :user:`marcelotduarte`
#)  chore: happy new year [ci skip] (:pr:`2765`) :user:`marcelotduarte`
#)  hooks: fix pyqt5 on conda-forge (:pr:`2763`) :user:`marcelotduarte`
#)  chore: add some fail-safe checks (:pr:`2764`) :user:`marcelotduarte`
#)  fix: #2680 regression (:pr:`2762`) :user:`marcelotduarte`
#)  hooks: update pyqt5/pyqt6/pyside6 resources [ci skip] (:pr:`2761`) :user:`marcelotduarte`
#)  build-wheel: build only universal2 wheels on macOS (:pr:`2760`) :user:`marcelotduarte`
#)  hooks: fix for torch and triton backends (:pr:`2751`) :user:`marcelotduarte`
#)  hooks: fix for pytorch/nvidia/torchmetrics (:pr:`2750`) :user:`marcelotduarte`
#)  doc: Corrects a typo in `setup_script.rst` (:pr:`2757`) :user:`patocv2`
#)  ci: Publish to testpypi does not work on PR on a fork [ci skip] (:pr:`2758`) :user:`marcelotduarte`
#)  hooks: add shapely.py (:pr:`2749`) :user:`marcelotduarte`
#)  bases: update base executables and util module [ci skip] (:pr:`2756`) :user:`marcelotduarte`
#)  build-wheel: use uvx w/ bump-my-version and cibuildwheel (:pr:`2755`) :user:`marcelotduarte`
#)  chore: use pythoncapi_compat (:pr:`2754`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.6.9 to 7.6.10 (:pr:`2752`) :user:`dependabot`
#)  fix: three small fixes (:pr:`2748`) :user:`marcelotduarte`
#)  build-wheel: improve performance (:pr:`2747`) :user:`marcelotduarte`
#)  build(deps): bump astral-sh/setup-uv from 4 to 5 (:pr:`2744`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.28.3 to 0.29.0 (:pr:`2745`) :user:`dependabot`
#)  bases: update base executables and util module [ci skip] (:pr:`2746`) :user:`marcelotduarte`
#)  chore: use uv build and uvx (:pr:`2743`) :user:`marcelotduarte`
#)  chore: use private heap instead of stack for buffers (:pr:`2742`) :user:`marcelotduarte`
#)  fix: a segmentation fault in py313t (:pr:`2740`) :user:`marcelotduarte`
#)  tests: remove psutil to speedup tests up to 30% [ci skip] (:pr:`2741`) :user:`marcelotduarte`
#)  hooks: support opencv-python 4.10.x (including headless) (:pr:`2735`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.28.2 to 0.28.3 (:pr:`2739`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.28.1 to 0.28.2 (:pr:`2734`) :user:`dependabot`
#)  chore: use is_relative_to (py39+) to simplify code (:pr:`2732`) :user:`marcelotduarte`
#)  bases: update base executables and util module [ci skip] (:pr:`2731`) :user:`marcelotduarte`
#)  chore: cleanup (:pr:`2730`) :user:`marcelotduarte`
#)  chore: add support for Python 3.13 [macOS] (:pr:`2728`) :user:`marcelotduarte`
#)  chore: use stdlib importlib.metadata (:pr:`2727`) :user:`marcelotduarte`
#)  bases: PEP587 - Python Initialization Configuration (:pr:`2726`) :user:`marcelotduarte`
#)  chore: add support for Python 3.13 [Linux and Windows] (:pr:`2630`) :user:`marcelotduarte`
#)  doc: improve installation doc using tabs (:pr:`2725`) :user:`marcelotduarte`
#)  chore: move doc and tests requirements to directory of same name (:pr:`2724`) :user:`marcelotduarte`
#)  build(deps): update lief requirement from <0.16.0,>=0.12.0 to >=0.12.0,<0.17.0 (:pr:`2723`) :user:`dependabot`
#)  doc: improve doc for conda use and add warning to recomment its use (:pr:`2722`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2721`) :user:`pre-commit-ci`
#)  fix: support uv python in Linux (:pr:`2719`) :user:`marcelotduarte`
#)  doc: update .readthedocs.yaml [ci skip] (:pr:`2720`) :user:`marcelotduarte`
#)  hooks: fix support for Pillow in Linux (:pr:`2718`) :user:`marcelotduarte`
#)  chore: publish on testpypi on push (:pr:`2717`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.6.8 to 7.6.9 (:pr:`2716`) :user:`dependabot`
#)  chore: use python-coverage-comment-action to report coverage status (:pr:`2714`) :user:`marcelotduarte`
#)  build(deps): bump pytest from 8.3.3 to 8.3.4 (:pr:`2711`) :user:`dependabot`
#)  chore: get rid of codecov (:pr:`2712`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2710`) :user:`pre-commit-ci`
#)  build(deps): bump codecov/codecov-action from 4 to 5 (:pr:`2686`) :user:`dependabot`
#)  build-wheel: use multiple versions of a pr in testpipy (:pr:`2709`) :user:`marcelotduarte`
#)  fix: regression in module due to namespace changes (:pr:`2708`) :user:`marcelotduarte`
#)  ci: use download merge-multiple (:pr:`2707`) :user:`marcelotduarte`
#)  chore: send wheel from pr to testpypi (:pr:`2706`) :user:`marcelotduarte`
#)  chore: refactor build-wheel and ci (:pr:`2705`) :user:`marcelotduarte`
#)  ci: make rpm/deb tests do not xfail (:pr:`2700`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.6.7 to 7.6.8 (:pr:`2704`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.21.3 to 2.22.0 (:pr:`2703`) :user:`dependabot`
#)  build(deps): bump astral-sh/setup-uv from 3 to 4 (:pr:`2702`) :user:`dependabot`
#)  build-wheel: fix build sdist [ci skip] (:pr:`2699`) :user:`marcelotduarte`
#)  parser: use patchelf to get dependent file in arm [Linux] (:pr:`2695`) :user:`marcelotduarte`
#)  build-wheel: fix the build number (:pr:`2698`) :user:`marcelotduarte`
#)  pre-commit: update ruff code to new schema in validate-pyproject-schema-store 2024.11.22 (:pr:`2697`) :user:`marcelotduarte`
#)  build-wheel: fix the dev suffix (:pr:`2696`) :user:`marcelotduarte`
#)  Bump version: 7.3.0-dev0 → 7.3.0-dev.1 [ci skip] (:pr:`2694`) :user:`marcelotduarte`
#)  freezer: fix rpath [linux] (:pr:`2693`) :user:`marcelotduarte`
#)  build-wheel: Publish package to TestPyPI (:pr:`2689`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2692`) :user:`pre-commit-ci`
#)  Fix namespace package containing extensions (:pr:`2680`) :user:`sankilkis`
#)  build(deps): bump coverage from 7.6.5 to 7.6.7 (:pr:`2690`) :user:`dependabot`
#)  hooks: cleanup and reorganization (:pr:`2688`) :user:`marcelotduarte`
#)  setup: small fixes (:pr:`2687`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.6.4 to 7.6.5 (:pr:`2685`) :user:`dependabot`
#)  ci: use_oidc with codecov (:pr:`2684`) :user:`marcelotduarte`
#)  setup: copy pre-built bases on Windows (compilation is optional) (:pr:`2681`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2678`) :user:`pre-commit-ci`
#)  fix: use of build_exe --excludes with namespace packages (:pr:`2677`) :user:`marcelotduarte`
#)  fix: fix _get_top_dependencies to work on mingw (:pr:`2675`) :user:`marcelotduarte`
#)  hooks: support for pkg_resources from setuptools >= 71 (:pr:`2674`) :user:`marcelotduarte`
#)  hooks: numpy - resolve missing modules (:pr:`2670`) :user:`marcelotduarte`
#)  finder: fine-tuning the excludes list (:pr:`2669`) :user:`marcelotduarte`
#)  cli: add --verbose and --debug options (:pr:`2668`) :user:`marcelotduarte`
#)  fix: remove incorrect excludes (:pr:`2667`) :user:`marcelotduarte`
#)  fix: a more consise fix for namespace packages (:pr:`2665`) :user:`marcelotduarte`
#)  hooks: zoneinfo has an error not caught by a typo in tests (:pr:`2666`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2662`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.28.0 to 0.28.1 (:pr:`2661`) :user:`dependabot`
#)  chore: use convenient functions from stdlib that exist since 3.9 (:pr:`2658`) :user:`marcelotduarte`
#)  build(deps): bump pytest-cov from 5.0.0 to 6.0.0 (:pr:`2657`) :user:`dependabot`
#)  hooks: add fontTools (:pr:`2656`) :user:`marcelotduarte`
#)  hooks: fix for pymupdf 1.24.11+ (:pr:`2655`) :user:`marcelotduarte`
#)  cli: #2439 complementary fix on windows (:pr:`2654`) :user:`marcelotduarte`
#)  bases: update base executables and util module [ci skip] (:pr:`2652`) :user:`marcelotduarte`
#)  fix: After #2624 'Load python3.dll if it is on the target dir' (:pr:`2651`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2650`) :user:`pre-commit-ci`
#)  hooks: sets the alias for os.path (:pr:`2649`) :user:`marcelotduarte`
#)  hooks: optimize/improve more modules (:pr:`2648`) :user:`marcelotduarte`
#)  hooks: optimize/improve some modules (:pr:`2647`) :user:`marcelotduarte`
#)  chore: use uv with cibuildwheel [ci skip] (:pr:`2645`) :user:`marcelotduarte`
#)  hooks: optimize pyzmq, setuptools and pkg_resources (:pr:`2643`) :user:`marcelotduarte`
#)  finder: improve the report of missing modules (:pr:`2639`) :user:`marcelotduarte`
#)  bdist_dmg: catch errors when resource is busy (:pr:`2640`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2637`) :user:`pre-commit-ci`
#)  Enable github sponsor [ci skip] (:pr:`2638`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.6.3 to 7.6.4 (:pr:`2636`) :user:`dependabot`
#)  fix: cache only `distribution.requires` that are evaluated in the environment (:pr:`2634`) :user:`marcelotduarte`
#)  hooks: improve pyzmq (:pr:`2635`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.27.0 to 0.28.0 (:pr:`2633`) :user:`dependabot`
#)  freezer: include_msvcr now uses Redistributable files (:pr:`2451`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.6.2 to 7.6.3 (:pr:`2626`) :user:`dependabot`
#)  hooks: pydantic - #2610 missing file (:pr:`2628`) :user:`marcelotduarte`
#)  chore: simplify code using _compat and removing not required class (:pr:`2627`) :user:`marcelotduarte`
#)  freezer: Optimize the search for dependencies (:pr:`2624`) :user:`marcelotduarte`
#)  ci: migrate to astral-sh/setup-uv with cache (:pr:`2623`) :user:`marcelotduarte`
#)  tests: fix tkinter test in older macOS (:pr:`2622`) :user:`marcelotduarte`
#)  freezer: improve the use of rpath [linux] (:pr:`2621`) :user:`marcelotduarte`
#)  freezer: change the order to fix bugs with patchelf (:pr:`2620`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.6.1 to 7.6.2 (:pr:`2619`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.21.2 to 2.21.3 (:pr:`2618`) :user:`dependabot`
#)  build(deps-dev): bump pre-commit from 4.0.0 to 4.0.1 (:pr:`2617`) :user:`dependabot`
#)  build(deps): bump sphinx-tabs from 3.4.5 to 3.4.7 (:pr:`2616`) :user:`dependabot`
#)  build(deps-dev): bump blacken-docs from 1.18.0 to 1.19.0 (:pr:`2615`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2614`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pre-commit from 3.8.0 to 4.0.0 (:pr:`2613`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.26.1 to 0.27.0 (:pr:`2612`) :user:`dependabot`
#)  hooks: update pydantic hook and fix the sample (:pr:`2610`) :user:`marcelotduarte`
#)  module: preserve entry_points.txt from .egg-info (:pr:`2609`) :user:`cluck`
#)  build(deps-dev): bump cibuildwheel from 2.21.1 to 2.21.2 (:pr:`2605`) :user:`dependabot`
#)  build(deps): bump sphinx-new-tab-link from 0.6.0 to 0.6.1 (:pr:`2598`) :user:`dependabot`
#)  chore: Drop Python 3.8 (:pr:`2607`) :user:`marcelotduarte`
#)  Bump version: 7.2.3 → 7.3.0-dev0 [ci skip] (:pr:`2606`) :user:`marcelotduarte`
#)  hooks: refactor tkinter - add tests (:pr:`2604`) :user:`marcelotduarte`
#)  hooks: refactor pytz (:pr:`2603`) :user:`marcelotduarte`
#)  Bump version: 7.2.3-dev0 → 7.2.3 [ci skip] :user:`marcelotduarte`
#)  ci: remove pre-commit GHA workflow in favor of pre-commit.ci (:pr:`2602`) :user:`marcelotduarte`
#)  hooks: add urlib and fix pkg_resources (:pr:`2601`) :user:`marcelotduarte`
#)  samples: fix pycountry sample for pycountry 23+ (:pr:`2600`) :user:`marcelotduarte`
#)  hooks: support scipy 1.14 in zip library (:pr:`2597`) :user:`marcelotduarte`
#)  hooks: add VTK (vtkmodules) (:pr:`2595`) :user:`marcelotduarte`
#)  hooks: zoneinfo refactored - add tests (:pr:`2592`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2594`) :user:`pre-commit-ci`
#)  build_exe: fix include_path option (:pr:`2591`) :user:`marcelotduarte`
#)  hooks: torch - fix duplicate files (:pr:`2587`) :user:`marcelotduarte`
#)  freezer: fix reporting missing dependencies (:pr:`2590`) :user:`marcelotduarte`
#)  Bump version: 7.2.2 → 7.2.3-dev0 [ci skip] (:pr:`2589`) :user:`marcelotduarte`
#)  hooks: numpy - fix #2586 regression in windows (:pr:`2588`) :user:`marcelotduarte`
#)  hooks: numpy - fix duplicate files (:pr:`2586`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2585`) :user:`pre-commit-ci`
#)  Bump version: 7.2.1 → 7.2.2 [ci skip] (:pr:`2584`) :user:`marcelotduarte`
#)  executable: target_name does not need to be an identifier to be a valid filename (:pr:`2583`) :user:`marcelotduarte`
#)  cli: undeprecated --target-dir (:pr:`2582`) :user:`marcelotduarte`
#)  hooks: add pymupdf (:pr:`2581`) :user:`marcelotduarte`
#)  hooks: pkg_resources from setuptools >= 71 does not uses _vendor (:pr:`2580`) :user:`marcelotduarte`
#)  hooks: fix copy of files to wrong directories (qt) (:pr:`2578`) :user:`marcelotduarte`
#)  hooks: fix numpy/mkl in conda (:pr:`2579`) :user:`marcelotduarte`
#)  hooks: fix qml support for qt hooks (:pr:`2577`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.21.0 to 2.21.1 (:pr:`2573`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2571`) :user:`pre-commit-ci`
#)  build(deps): update setuptools requirement from <75,>=65.6.3 to >=65.6.3,<76 (:pr:`2569`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.26.0 to 0.26.1 (:pr:`2570`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.20.0 to 2.21.0 (:pr:`2567`) :user:`dependabot`
#)  bases: update base executables and util module [ci skip] (:pr:`2566`) :user:`marcelotduarte`
#)  Bump version: 7.2.0 → 7.2.1 [ci skip] (:pr:`2565`) :user:`marcelotduarte`
#)  build(deps): bump pytest from 8.3.2 to 8.3.3 (:pr:`2562`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2561`) :user:`pre-commit-ci`
#)  hooks: add tortoise-orm (:pr:`2564`) :user:`marcelotduarte`
#)  hooks: fix regression in qt windows (:pr:`2563`) :user:`marcelotduarte`
#)  build(deps): bump sphinx-new-tab-link from 0.5.3 to 0.6.0 (:pr:`2558`) :user:`dependabot`
#)  build(deps): update setuptools requirement (:pr:`2556`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2550`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.25.1 to 0.26.0 (:pr:`2549`) :user:`dependabot`
#)  build(deps): bump sphinx-new-tab-link from 0.5.2 to 0.5.3 (:pr:`2547`) :user:`dependabot`
#)  ci: run pytest on build wheels (instead of editable wheels) (:pr:`2555`) :user:`marcelotduarte`
#)  setup: do not copy libraries in develop mode (:pr:`2543`) :user:`marcelotduarte`
#)  docs: use brackets for the default value of option arguments (:pr:`2541`) :user:`marcelotduarte`
#)  build(deps,docs): update python dependencies (:pr:`2540`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.25.0 to 0.25.1 (:pr:`2538`) :user:`dependabot`
#)  build(deps): use setuptools >= 70.1 to build (get rid of wheel) (:pr:`2539`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.24.3 to 0.25.0 (:pr:`2537`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2536`) :user:`pre-commit-ci`
#)  build(deps-dev): bump cibuildwheel from 2.19.2 to 2.20.0 (:pr:`2535`) :user:`dependabot`
#)  build(deps): bump coverage from 7.6.0 to 7.6.1 (:pr:`2533`) :user:`dependabot`
#)  bases: fix regression because the order used by clang-format (:pr:`2530`) :user:`marcelotduarte`
#)  bdist_rpm: fix use of 'cxfreeze bdist_rpm' command (:pr:`2529`) :user:`marcelotduarte`
#)  build(deps): bump sphinx-new-tab-link from 0.5.1 to 0.5.2 (:pr:`2528`) :user:`dependabot`
#)  pre-commit: use clang-format (:pr:`2525`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2524`) :user:`pre-commit-ci`
#)  build(deps): update setuptools requirement from <72,>=65.6.3 to >=65.6.3,<73 (:pr:`2523`) :user:`dependabot`
#)  build(deps): bump sphinx-new-tab-link from 0.5.0 to 0.5.1 (:pr:`2522`) :user:`dependabot`
#)  build(deps): prepare for setuptools stop vendoring packages (:pr:`2521`) :user:`marcelotduarte`
#)  build(deps): bump pytest from 8.3.1 to 8.3.2 (:pr:`2520`) :user:`dependabot`
#)  parser: add compatibility with lief 0.15.x (:pr:`2519`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2517`) :user:`pre-commit-ci`
#)  build(deps): bump pytest from 8.2.2 to 8.3.1 (:pr:`2516`) :user:`dependabot`
#)  build_exe: MingW and posix systems silently ignore include_msvcr option (:pr:`2514`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.24.2 to 0.24.3 (:pr:`2511`) :user:`dependabot`
#)  build(deps): update setuptools requirement from <71,>=65.6.3 to >=65.6.3,<72 (:pr:`2512`) :user:`dependabot`
