7.x releases
############

Version 7.2 (Jul 16)
----------------------

#)  hooks: the optimized mode is the default for pip installations (:pr:`2500`) :user:`marcelotduarte`
#)  bdist_rpm: drop rpm2_mode and refactor spec_file (:pr:`2488`) :user:`marcelotduarte`
#)  bdist_appimage: remove zip file, propagate options, fixes docs (:pr:`2463`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.5.4 to 7.6.0 (:pr:`2498`) :user:`dependabot`
#)  bdist_msi: add license for msi (:pr:`2472`) :user:`nick`
#)  bdist_dmg: add dmgbuild as a dependency to improve mac dmg (:pr:`2442`) :user:`nick`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2494`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.24.1 to 0.24.2 (:pr:`2492`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.19.1 to 2.19.2 (:pr:`2491`) :user:`dependabot`
#)  tests: make test pass in conda-forge [osx, linux] (:pr:`2490`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2487`) :user:`pre-commit-ci`
#)  build(deps): bump sphinx-new-tab-link from 0.4.0 to 0.5.0 (:pr:`2486`) :user:`dependabot`
#)  exception: Only re-export setuptools errors to avoid exceptions not handled correctly (:pr:`2485`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.24.0 to 0.24.1 (:pr:`2484`) :user:`dependabot`
#)  hooks: add multiprocess (a multiprocessing fork) (:pr:`2475`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.23.0 to 0.24.0 (:pr:`2481`) :user:`dependabot`
#)  sample: add sample for Gtk (:pr:`2364`) :user:`cedk`
#)  chore: use setup-python-uv-action to cache uv packages (:pr:`2482`) :user:`marcelotduarte`
#)  tests: make tests pass on mingw (:pr:`2476 regression) (#2480`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2479`) :user:`pre-commit-ci`
#)  build(deps): bump coverage from 7.5.3 to 7.5.4 (:pr:`2477`) :user:`dependabot`
#)  tests: improve _compat to use in tests (:pr:`2476`) :user:`marcelotduarte`
#)  tests: fix test_cli in archlinux (:pr:`2470`) :user:`marcelotduarte`
#)  build(deps): bump update setuptools requirement to >=65.6.3,<71 (:pr:`2468`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2464`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.22.0 to 0.23.0 (:pr:`2462`) :user:`dependabot`
#)  hooks: support numpy 2.0 (:pr:`2466`) :user:`marcelotduarte`
#)  Bump version: 7.1.0-post0 → 7.1.1 [ci skip] (:pr:`2461`) :user:`marcelotduarte`
#)  hooks: improve scikit-image (:pr:`2460`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.19.0 to 2.19.1 (:pr:`2458`) :user:`dependabot`
#)  hooks: add rasterio (:pr:`2455`) :user:`marcelotduarte`
#)  hooks: fix #2382 regression / improve tests and docs (:pr:`2443`) :user:`marcelotduarte`
#)  hooks: avoid exception when distribution is none (:pr:`2452`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.21.1 to 0.22.0 (:pr:`2450`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2448`) :user:`pre-commit-ci`
#)  build(deps-dev): bump cibuildwheel from 2.18.1 to 2.19.0 (:pr:`2447`) :user:`dependabot`
#)  doc: small revision of development/index [ci skip] (:pr:`2446`) :user:`marcelotduarte`
#)  bdist_rpm: Fix string concat error due to order of op for + and or in RPM (:pr:`2444`) :user:`nicktindle`
#)  cli: fix sys.path for cxfreeze command line (:pr:`2439`) :user:`marcelotduarte`
#)  build(deps): bump pytest from 8.2.1 to 8.2.2 (:pr:`2437`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2434`) :user:`pre-commit-ci`
#)  Bump version: 7.1.0 → 7.1.0-post0 [ci skip] (:pr:`2432`) :user:`marcelotduarte`
#)  doc: msvc faq revision [ci skip] (:pr:`2429`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.5.2 to 7.5.3 (:pr:`2428`) :user:`dependabot`
#)  hooks: fix pygobject hook for Linux (:pr:`2425`) :user:`marcelotduarte`

Version 7.1 (May 26)
----------------------

#)  hooks: add mkl (:pr:`2420`) :user:`marcelotduarte`
#)  hooks: resolve dependencies to avoid symlink in numpy/mkl/blas conda linux (:pr:`2419`) :user:`marcelotduarte`
#)  module: fix distribution installer multiline (:pr:`2418`) :user:`marcelotduarte`
#)  ci: add test to do more 'parser' and 'module' coverage (:pr:`2416`) :user:`marcelotduarte`
#)  freezer: resolve symlinks to always copy the source (:pr:`2415`) :user:`marcelotduarte`
#)  build(deps): update setuptools requirement from <70,>=62.6 to >=62.6,<71 (:pr:`2413`) :user:`dependabot`
#)  freezer: resolve dependencies to avoid symlink [linux] (:pr:`2410`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2409`) :user:`pre-commit-ci`
#)  build(deps-dev): bump cibuildwheel from 2.18.0 to 2.18.1 (:pr:`2408`) :user:`dependabot`
#)  build(deps): bump pytest from 8.2.0 to 8.2.1 (:pr:`2407`) :user:`dependabot`
#)  hooks: support for numpy + oneMKL using pip windows (:pr:`2405`) :user:`marcelotduarte`
#)  hooks: support for numpy+mkl on conda linux (:pr:`2404`) :user:`marcelotduarte`
#)  module: improve version method and add new methods (:pr:`2403`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.21.0 to 0.21.1 (:pr:`2399`) :user:`dependabot`
#)  bdist_deb: catch a cpio 2.13 bug (:pr:`2402`) :user:`marcelotduarte`
#)  chore: use uv pip to make installing packages faster (:pr:`2397`) :user:`marcelotduarte`
#)  tests: xfail bdist_dmg when "Resource busy" [macOS] (:pr:`2396`) :user:`marcelotduarte`
#)  doc: use uv pip (:pr:`2395`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2394`) :user:`pre-commit-ci`
#)  build(deps-dev): bump cibuildwheel from 2.17.0 to 2.18.0 (:pr:`2393`) :user:`dependabot`
#)  hooks: add wayland Qt plugins automatically (:pr:`2391`) :user:`marcelotduarte`
#)  hooks: add missing Qt plugins and translations (:pr:`2390`) :user:`marcelotduarte`
#)  hooks: update plugins and translations for qt 6.7 (:pr:`2389`) :user:`marcelotduarte`
#)  doc: add faq 'Removing the MAX_PATH Limitation' (:pr:`2388`) :user:`marcelotduarte`
#)  chore: use compile() with dont_inherit and optimize (:pr:`2387`) :user:`marcelotduarte`
#)  hooks: additional translations to qt hooks (:pr:`2386`) :user:`marcelotduarte`
#)  fix: global of main module to work better with multiprocessing (:pr:`2385`) :user:`marcelotduarte`
#)  hooks: improve multiprocessing hook to work with pytorch (:pr:`2382`) :user:`marcelotduarte`
#)  build_exe: add new option --zip-filename (:pr:`2379`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2381`) :user:`pre-commit-ci`
#)  build(deps): bump coverage from 7.5.0 to 7.5.1 (:pr:`2380`) :user:`dependabot`
#)  build-wheel: reactivate universal2 wheels for macOS (:pr:`2378`) :user:`marcelotduarte`
#)  hooks: add pygobject (:pr:`2375`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.20.3 to 0.21.0 (:pr:`2377`) :user:`dependabot`
#)  build(deps): bump pytest-xdist[psutil] from 3.5.0 to 3.6.1 (:pr:`2370`) :user:`dependabot`
#)  build(deps): bump pytest from 8.1.2 to 8.2.0 (:pr:`2372`) :user:`dependabot`
#)  build(deps): bump myst-parser from 3.0.0 to 3.0.1 (:pr:`2371`) :user:`dependabot`
#)  samples: adapt code to support ruff rules (:pr:`2369`) :user:`marcelotduarte`
#)  build(deps-dev): update pytest to 8.1.2, revert pyetst-xdist to 3.5.0 (:pr:`2368`) :user:`marcelotduarte`
#)  tests: make msys2/mingw tests pass (:pr:`2367`) :user:`marcelotduarte`
#)  bdist_msi: ignore warning 'msilib' is deprecated (:pr:`2366`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.20.2 to 0.20.3 (:pr:`2365`) :user:`dependabot`
#)  hooks: fix unbound variable in load_subprocess under MINGW (:pr:`2363`) :user:`cedk`
#)  ci: try to catch a issue with macos (:pr:`2360`) :user:`marcelotduarte`
#)  hooks: Recompile the numpy.core.overrides module to limit optimization (:pr:`2358`) :user:`marcelotduarte`
#)  hooks: fix regression in msys2 (:pr:`2357`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.4.4 to 7.5.0 (:pr:`2355`) :user:`dependabot`
#)  ci: CI tests fails using macos-latest (:pr:`2359`) :user:`marcelotduarte`
#)  tests: add command line tests for build_exe (:pr:`2353`) :user:`marcelotduarte`
#)  build(deps): bump myst-parser from 2.0.0 to 3.0.0 (:pr:`2351`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.20.1 to 0.20.2 (:pr:`2350`) :user:`dependabot`
#)  tests: xfail bdist_dmg if resource is busy (:pr:`2352`) :user:`marcelotduarte`
#)  build(deps): bump pluggy from 1.4.0 to 1.5.0 (:pr:`2348`) :user:`dependabot`
#)  Bump version: 7.0.0 → 7.1.0-dev0 [ci skip] (:pr:`2349`) :user:`marcelotduarte`

Version 7.0 (April 21)
----------------------

#)  hooks: support numpy in python 3.12 (:pr:`2345`) :user:`marcelotduarte`
#)  test: add simple test for bdist_mac (:pr:`2343`) :user:`marcelotduarte`
#)  fix: regression in _pre_copy_hook (Linux) (:pr:`2342`) :user:`marcelotduarte`
#)  build(deps): update dev dependencies (:pr:`2341`) :user:`marcelotduarte`
#)  parser: show what patchelf is doing if silent is off (:pr:`2340`) :user:`marcelotduarte`
#)  initscripts: use of __loader__ is deprecated (:pr:`2338`) :user:`marcelotduarte`
#)  tests: add test_hooks_pandas.py (:pr:`2336`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.20.0 to 0.20.1 (:pr:`2337`) :user:`dependabot`
#)  test: an expected exception should not be treated as an expected failure (:pr:`2334`) :user:`marcelotduarte`
#)  fix: coverage report usage and omit option (:pr:`2333`) :user:`marcelotduarte`
#)  test: add a linux binary wheel test in ci (:pr:`2332`) :user:`marcelotduarte`
#)  chore: generate multiple files for requirements (:pr:`2330`) :user:`marcelotduarte`
#)  doc: Correct some typographical errors and grammar errors (:pr:`2328`) :user:`marcelotduarte`
#)  doc: show builtdist command as toctree and clickable in the table (:pr:`2327`) :user:`marcelotduarte`
#)  doc: separates bdist commands to nest them in builtdist (:pr:`2325`) :user:`marcelotduarte`
#)  doc: show pyproject.toml as first example (:pr:`2326`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2324`) :user:`pre-commit-ci`
#)  chore: move License to the project root dir (:pr:`2323`) :user:`marcelotduarte`
#)  doc: fix furo edit button [ci skip] (:pr:`2322`) :user:`marcelotduarte`
#)  docs: add 'Creating Built Distributions' (:pr:`2321`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.19.3 to 0.20.0 (:pr:`2320`) :user:`dependabot`
#)  chore: refactor internal modules (:pr:`2319`) :user:`marcelotduarte`
#)  build(deps): pin dev dependencies (:pr:`2318`) :user:`marcelotduarte`
#)  bases: update base executables and util module [ci skip] (:pr:`2317`) :user:`marcelotduarte`
#)  chore: remove deprecated option in 'build' command (:pr:`2316`) :user:`marcelotduarte`
#)  Bump version: 6.16.0-dev12 → 7.0.0-rc0 [ci skip] (:pr:`2315`) :user:`marcelotduarte`
#)  chore: remove unused class (:pr:`2314`) :user:`marcelotduarte`
#)  build(deps-dev): bump pytest-mock from 3.12.0 to 3.14.0 (:pr:`2311`) :user:`dependabot`
#)  tests: add TYPE_CHECKING to coverage excludes (:pr:`2310`) :user:`marcelotduarte`
#)  chore: improve annotation (using ruff to check) (:pr:`2309`) :user:`marcelotduarte`
#)  chore: adapt code to support ruff 'S' rules (:pr:`2308`) :user:`marcelotduarte`
#)  chore: improve type checking (w/ help of ruff) (:pr:`2307`) :user:`marcelotduarte`
#)  build(deps-dev): bump sphinx-new-tab-link from 0.3.1 to 0.4.0 (:pr:`2306`) :user:`dependabot`
#)  chore: use more ruff lint rules (:pr:`2305`) :user:`marcelotduarte`
#)  chore: enable ruff 'EM' ruleset (:pr:`2304`) :user:`marcelotduarte`
#)  build: fix for Python 3.12 Ubuntu Linux 24.04 (Noble Nimbat) (:pr:`2303`) :user:`marcelotduarte`
#)  hooks: support tensorflow plugins (:pr:`2302`) :user:`marcelotduarte`
#)  hooks: add easyocr and torchvision (also update skickit-image and pytorch) (:pr:`2286`) :user:`marcelotduarte`
#)  build(deps-dev): bump coverage from 7.4.3 to 7.4.4 (:pr:`2301`) :user:`dependabot`
#)  build-wheel: use macos-14 (native arm) with cibuildwheel (:pr:`2299`) :user:`marcelotduarte`
#)  build(deps): update wheel requirement from <=0.42.0,>=0.38.4 to >=0.38.4,<=0.43.0 (:pr:`2298`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.16.5 to 2.17.0 (:pr:`2297`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.18.3 to 0.19.0 (:pr:`2296`) :user:`dependabot`
#)  cli: restore more deprecated options (:pr:`2295`) :user:`marcelotduarte`
#)  build(deps-dev): bump ruff-pre-commit 0.3.2 [ci skip] (:pr:`2294`) :user:`marcelotduarte`
#)  build(deps-dev): bump sphinx-new-tab-link from 0.3.0 to 0.3.1 (:pr:`2292`) :user:`dependabot`
#)  build(deps-dev): bump pytest from 8.0.2 to 8.1.1 (:pr:`2291`) :user:`dependabot`
#)  build(deps-dev): bump pytest-timeout from 2.2.0 to 2.3.1 (:pr:`2289`) :user:`dependabot`
#)  doc: improve the code_layout a bit (:pr:`2288`) :user:`marcelotduarte`
#)  hooks: support pytorch 2.2 (:pr:`2281`) :user:`marcelotduarte`
#)  docs: update msvcr links (:pr:`2284`) :user:`marcelotduarte`
#)  build(deps-dev): bump sphinx-new-tab-link from 0.2.3 to 0.3.0 (:pr:`2282`) :user:`dependabot`
#)  build(deps-dev): bump sphinx-new-tab-link from 0.2.2 to 0.2.3 (:pr:`2279`) :user:`dependabot`
#)  build(deps-dev): bump coverage from 7.4.2 to 7.4.3 (:pr:`2278`) :user:`dependabot`
#)  build(deps-dev): bump pytest from 8.0.1 to 8.0.2 (:pr:`2277`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.17.4 to 0.18.3 (:pr:`2276`) :user:`dependabot`
#)  bdist_msi: remove unused code (:pr:`2270`) :user:`marcelotduarte`
#)  build(deps-dev): bump coverage from 7.4.1 to 7.4.2 (:pr:`2271`) :user:`dependabot`
#)  tests: improve bdist_msi tests and samples (:pr:`2269`) :user:`marcelotduarte`
#)  chore: use only 'ruff' as a linter and formatter (:pr:`2268`) :user:`marcelotduarte`
#)  build(deps): support lief 0.14.x (:pr:`2267`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2266`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pytest from 8.0.0 to 8.0.1 (:pr:`2265`) :user:`dependabot`
#)  freezer: remove dead code (not used in py38+) (:pr:`2263`) :user:`marcelotduarte`
#)  tests: improve a bit build_exe and freezer tests (:pr:`2262`) :user:`marcelotduarte`
#)  bdist_deb: fix call to bdist_rpm, improve tests (:pr:`2260`) :user:`marcelotduarte`
#)  pre-commit: use validate-pyproject-schema-store (:pr:`2258`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2257`) :user:`pre-commit-ci`
#)  build(deps-dev): bump furo from 2023.9.10 to 2024.1.29 (:pr:`2256`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.17.3 to 0.17.4 (:pr:`2255`) :user:`dependabot`
#)  tests: add more tests for freezer (:pr:`2254`) :user:`marcelotduarte`
#)  build-exe: adds include_path option (formerly in cli) (:pr:`2253`) :user:`marcelotduarte`
#)  fix: #2242 introduced a regression in install_exe (:pr:`2250`) :user:`marcelotduarte`
#)  fix: remove misuse of packages in setuptools.setup (:pr:`2249`) :user:`marcelotduarte`
#)  tests: add more tests for bdist_msi (:pr:`2248`) :user:`marcelotduarte`
#)  chore: add support for pyproject.toml (tool.cxfreeze) (:pr:`2244`) :user:`marcelotduarte`
#)  build(deps): bump codecov/codecov-action from 3 to 4 (:pr:`2238`) :user:`dependabot`
#)  build(deps-dev): bump sphinx-new-tab-link from 0.2.1 to 0.2.2 (:pr:`2245`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2243`) :user:`pre-commit-ci`
#)  fix: incorrect metadata usage in install/install_exe (:pr:`2242`) :user:`marcelotduarte`
#)  tests: improve coverage tests for linux (:pr:`2241`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.16.4 to 2.16.5 (:pr:`2237`) :user:`dependabot`
#)  ci: add specific coverage test for linux (:pr:`2239`) :user:`marcelotduarte`
#)  fix: coverage report extra tests (:pr:`2236`) :user:`marcelotduarte`
#)  chore: rearranges and sort some settings (:pr:`2235`) :user:`marcelotduarte`
#)  chore: improve the use of coverage (:pr:`2233`) :user:`marcelotduarte`
#)  build(deps-dev): bump black 2024 (:pr:`2230`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.16.2 to 2.16.4 (:pr:`2229`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.17.1 to 0.17.3 (:pr:`2228`) :user:`dependabot`
#)  build(deps-dev): bump pytest from 7.4.4 to 8.0.0 (:pr:`2227`) :user:`dependabot`
#)  tests: add some freezer tests (:pr:`2226`) :user:`marcelotduarte`
#)  executable: new option --uac-uiaccess (:pr:`2135`) :user:`marcelotduarte`
#)  chore: add options to pre-commit (:pr:`2225`) :user:`marcelotduarte`
#)  tests: test build_exe options silent,silent-level and build_exe (:pr:`2224`) :user:`marcelotduarte`
#)  tests: target_dir "starts in a clean directory" (:pr:`2223`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.17.0 to 0.17.1 (:pr:`2222`) :user:`dependabot`
#)  winversioninfo: comments length must be limited to fit WORD (:pr:`2220`) :user:`marcelotduarte`
#)  tests: add tests for __main__ and cli (:pr:`2219`) :user:`marcelotduarte`
#)  build(deps-dev): bump pluggy from 1.3.0 to 1.4.0 (:pr:`2217`) :user:`dependabot`
#)  parser: minor fix to support lief 0.14 (:pr:`2216`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2215`) :user:`pre-commit-ci`
#)  build(deps-dev): bump sphinx-tabs from 3.4.4 to 3.4.5 (:pr:`2214`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.16.2 to 0.17.0 (:pr:`2213`) :user:`dependabot`
#)  winversioninfo: fix version string and improve coverage/tests (:pr:`2211`) :user:`marcelotduarte`
#)  chore: Update copyright year and license (:pr:`2209`) :user:`marcelotduarte`
#)  docs: open external links in new tab (:pr:`2208`) :user:`marcelotduarte`
#)  hooks: add pyproj (:pr:`2207`) :user:`marcelotduarte`
#)  winmsvcr: extend support for VS 2022 (:pr:`2204`) :user:`marcelotduarte`
#)  hooks: opencv-python - minor fixes (:pr:`2206`) :user:`marcelotduarte`
#)  freezer: improve/fixes validate_executable (:pr:`2205`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2202`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.16.1 to 0.16.2 (:pr:`2201`) :user:`dependabot`
#)  tests: minor tweaks - part 2 (:pr:`2198`) :user:`marcelotduarte`
#)  tests: minor tweaks - part 1 (:pr:`2197`) :user:`marcelotduarte`
#)  build(deps-dev): bump pre-commit up to 3.6.0 and sphinx up to 7.2.6 (:pr:`2196`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2195`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.16.0 to 0.16.1 (:pr:`2194`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.15.4 to 0.16.0 (:pr:`2191`) :user:`dependabot`
#)  tests: simplify more tests using run_command (:pr:`2189`) :user:`marcelotduarte`
#)  tests: simplify test using a run_command (:pr:`2187`) :user:`marcelotduarte`
#)  build(deps-dev): bump pytest from 7.4.3 to 7.4.4 (:pr:`2188`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.15.3 to 0.15.4 (:pr:`2186`) :user:`dependabot`
#)  setup script: add an extension to executable icon that is valid across OS (:pr:`2185`) :user:`marcelotduarte`
#)  setup script: pre-defined values for base are valid in all OS (:pr:`2184`) :user:`marcelotduarte`
#)  setup script: extend executables keyword to support more types (:pr:`2182`) :user:`marcelotduarte`
#)  bdist_appimage: build Linux AppImage format [new feature] (:pr:`2050`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2181`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.15.1 to 0.15.3 (:pr:`2178`) :user:`dependabot`
#)  build-wheel: fix update_bases' ref and cleanup publish (:pr:`2176`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2175`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.12.0 to 0.15.1 (:pr:`2174`) :user:`dependabot`
#)  Bump version: 6.16.0-dev11 → 6.16.0-dev12 [ci skip] (:pr:`2173`) :user:`marcelotduarte`
#)  bdist_mac: create symlink between folders specified by user under Resources (:pr:`2169`) :user:`admin`
#)  fix: #2139 introduced a regression [macos] (:pr:`2172`) :user:`marcelotduarte`
#)  hooks: add AV and PyAV (:pr:`2165`) :user:`marcelotduarte`
#)  build: fix build_wheel (after #2162 and #2163) (:pr:`2170`) :user:`marcelotduarte`
#)  build(deps): bump actions/download-artifact from 3 to 4 (:pr:`2163`) :user:`dependabot`
#)  build(deps): bump actions/upload-artifact from 3 to 4 (:pr:`2162`) :user:`dependabot`
#)  build(deps): bump github/codeql-action from 2 to 3 (:pr:`2160`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2157`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pylint from 3.0.2 to 3.0.3 (:pr:`2156`) :user:`dependabot`
#)  build(deps): bump actions/setup-python from 4 to 5 (:pr:`2155`) :user:`dependabot`
#)  Replace SetDllDirectory by AddDllDirectory (:pr:`2144`) :user:`dev`
#)  Bump version: 6.16.0-dev10 → 6.16.0-dev11 [ci skip] (:pr:`2151`) :user:`marcelotduarte`
#)  fix: pthread missing for building in FreeBSD (:pr:`2150`) :user:`marcelotduarte`
#)  build(deps): bump wheel from 0.41.3 to 0.42.0 (:pr:`2148`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.11.0 to 0.12.0 (:pr:`2147`) :user:`dependabot`
#)  chore: switch to bump-my-version (:pr:`2146`) :user:`marcelotduarte`
#)  bdist_mac: apply the style of other bdist modules (:pr:`2139`) :user:`marcelotduarte`
#)  hooks: add yt_dlp (:pr:`2145`) :user:`marcelotduarte`
#)  build(deps-dev): bump pytest-xdist[psutil] from 3.4.0 to 3.5.0 (:pr:`2143`) :user:`dependabot`
#)  build(deps): update setuptools requirement from <69,>=62.6 to >=62.6,<70 (:pr:`2141`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2142`) :user:`pre-commit-ci`
#)  freezer: Improve symlink support to work w/ macOS (:pr:`2138`) :user:`marcelotduarte`
#)  hooks: adds anyio, pyarrow and tiktoken (:pr:`2134`) :user:`marcelotduarte`
#)  chore: cosmetic and minor tweaks (:pr:`2137`) :user:`marcelotduarte`
#)  build_exe: raise exception on invalid build_exe option (:pr:`2132`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2130`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pytest-xdist[psutil] from 3.3.1 to 3.4.0 (:pr:`2129`) :user:`dependabot`
#)  samples: improve qt samples (:pr:`2128`) :user:`marcelotduarte`
#)  hooks: Support for PyQt5/PySide2 QtWebEngine in macOS (:pr:`2127`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2125`) :user:`pre-commit-ci`
#)  hooks: Support for PyQt6/PySide6 QtWebEngine in macOS (:pr:`2124`) :user:`marcelotduarte`
#)  hooks: use a different approach for pyqt6 in bdist_mac (:pr:`2123`) :user:`marcelotduarte`
#)  hooks: fix pyqt6 in bdist_mac (.app) (:pr:`2122`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2120`) :user:`pre-commit-ci`
#)  build(deps): bump wheel from 0.41.2 to 0.41.3 (:pr:`2119`) :user:`dependabot`
#)  build(deps-dev): bump pytest from 7.4.2 to 7.4.3 (:pr:`2115`) :user:`dependabot`
#)  "Bump version: 6.16.0-dev9 → 6.16.0-dev10 [ci skip]" (:pr:`2114`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2113`) :user:`pre-commit-ci`
#)  build(deps-dev): bump sphinx-tabs from 3.4.1 to 3.4.4 (:pr:`2112`) :user:`dependabot`
#)  build(deps-dev): bump pylint from 3.0.1 to 3.0.2 (:pr:`2111`) :user:`dependabot`
#)  hooks: fix qtwebengine in conda-forge (:pr:`2110`) :user:`marcelotduarte`
#)  hooks: fix qt.conf for pyqt [macos] (:pr:`2109`) :user:`marcelotduarte`
#)  hooks: tweaks to the debugging of qt hooks (:pr:`2108`) :user:`marcelotduarte`
#)  bdist_mac: move set_relative_reference_paths to build_exe (:pr:`2106`) :user:`marcelotduarte`
#)  darwintools: fix adhocsignature for universal2 machine (:pr:`2107`) :user:`marcelotduarte`
#)  bdist_mac: make symlink between Resources/share and Contents/MacOS (:pr:`2105`) :user:`marcelotduarte`
#)  parse: regression fix in get_dependent_files [windows] (:pr:`2104`) :user:`marcelotduarte`
#)  bdist_mac: skip text files in set_relative_reference_paths (:pr:`2102`) :user:`micah`
#)  build(deps-dev): bump pytest-mock from 3.11.1 to 3.12.0 (:pr:`2103`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2101`) :user:`pre-commit-ci`
#)  bases: update base executables and util module [ci skip] (:pr:`2100`) :user:`marcelotduarte`
#)  chore: update base executables and util module [ci skip] (:pr:`2099`) :user:`marcelotduarte`
#)  "Bump version: 6.16.0-dev8 → 6.16.0-dev9 [ci skip]" (:pr:`2098`) :user:`marcelotduarte`
#)  fix: issues with manifest and windows version (:pr:`2097`) :user:`marcelotduarte`
#)  build(deps-dev): bump pre-commit from 3.4.0 to 3.5.0 (:pr:`2096`) :user:`dependabot`
#)  hooks: add triton and support for pytorch 2.1 (:pr:`2090`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2092`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pytest-timeout from 2.1.0 to 2.2.0 (:pr:`2091`) :user:`dependabot`
#)  build(deps-dev): bump pylint from 3.0.0 to 3.0.1 (:pr:`2089`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.16.1 to 2.16.2 (:pr:`2085`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2082`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pylint from 2.17.6 to 3.0.0 (:pr:`2081`) :user:`dependabot`
#)  tests: use importorskip/skip at module level to skip early (:pr:`2084`) :user:`marcelotduarte`
#)  chore: rewrite some imports as absolute (:pr:`2083`) :user:`marcelotduarte`
#)  bdist_deb: add doc and tests (:pr:`2080`) :user:`marcelotduarte`
#)  doc: minor fixes (:pr:`2079`) :user:`marcelotduarte`
#)  bdist_deb: create an DEB distribution [new feature] (:pr:`2078`) :user:`marcelotduarte`
#)  bdist_rpm: remove unused options (:pr:`2077`) :user:`marcelotduarte`
#)  "Bump version: 6.16.0-dev7 → 6.16.0-dev8 [ci skip]" (:pr:`2076`) :user:`marcelotduarte`
#)  bdist_rpm: fix issue with install prefix (:pr:`2075`) :user:`marcelotduarte`
#)  hooks: initialize blas [numpy conda-forge] (:pr:`2074`) :user:`49456524+IperGiove`
#)  parser: exclude LD_PRELOAD to not include triggered dependencies (:pr:`2073`) :user:`marcelotduarte`
#)  hooks: add tidylib (:pr:`2072`) :user:`marcelotduarte`
#)  parser: use the internal path instead of sys.path (:pr:`2071`) :user:`marcelotduarte`
#)  fix: avoid false builtin modules developing in multi-environment (:pr:`2070`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.16.0 to 2.16.1 (:pr:`2069`) :user:`dependabot`
#)  hooks: move tkinter and tz data to share folder (:pr:`2067`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2066`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pylint from 2.17.5 to 2.17.6 (:pr:`2065`) :user:`dependabot`
#)  tests: minor tweaks (:pr:`2063`) :user:`marcelotduarte`
#)  build_exe: fix typo in command line boolean option 'include-msvcr' (:pr:`2062`) :user:`marcelotduarte`
#)  hooks: fix scipy windows (:pr:`2060`) :user:`marcelotduarte`
#)  doc: improve documentation for 'binary wheels' (:pr:`2059`) :user:`marcelotduarte`
#)  hooks: add numpy 1.26 (:pr:`2058`) :user:`marcelotduarte`
#)  hooks: fix numpy/scipy regression [mingw] (:pr:`2057`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.15.0 to 2.16.0 (:pr:`2056`) :user:`dependabot`
#)  hooks: add RNS (Reticulum) (:pr:`2053`) :user:`marcelotduarte`
#)  bdist_mac: Copy build_exe to Resources and move executables to MacOS (:pr:`2048`) :user:`marcelotduarte`
#)  hooks: fix numpy/scipy dylibs are included twice (:pr:`2038`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2055`) :user:`pre-commit-ci`
#)  "Bump version: 6.16.0-dev6 → 6.16.0-dev7 [ci skip]" (:pr:`2052`) :user:`marcelotduarte`
#)  icons: add Python icons (:pr:`2051`) :user:`marcelotduarte`
#)  Revert "build(deps): bump codecov/codecov-action from 3 to 4" (:pr:`2049`) :user:`marcelotduarte`
#)  build(deps): bump codecov/codecov-action from 3 to 4 (:pr:`2047`) :user:`dependabot`
#)  samples: small tweaks to demonstrate independent options (:pr:`2045`) :user:`marcelotduarte`
#)  build(deps): bump docker/setup-qemu-action from 2 to 3 (:pr:`2044`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2043`) :user:`pre-commit-ci`
#)  bdist_mac: small optimization on copy tree (:pr:`2040`) :user:`marcelotduarte`
#)  bdist_mac: fix duplicate lib in bdist_dmg [regression] (:pr:`2037`) :user:`marcelotduarte`
#)  hooks: improve numpy and pandas hooks (:pr:`2036`) :user:`marcelotduarte`
#)  build(deps-dev): bump pytest from 7.4.1 to 7.4.2 (:pr:`2035`) :user:`dependabot`
#)  "Bump version: 6.16.0-dev5 → 6.16.0-dev6 [ci skip]" (:pr:`2034`) :user:`marcelotduarte`
#)  doc: Building binary wheels (:pr:`2033`) :user:`marcelotduarte`
#)  hooks: add support for pandas 2.1.0 (:pr:`2032`) :user:`marcelotduarte`
#)  build-wheel: fix build and compatibility w/ build 1.0 (:pr:`2030`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2031`) :user:`pre-commit-ci`
#)  build(deps): bump actions/checkout from 3 to 4 (:pr:`2029`) :user:`dependabot`
#)  build(deps-dev): bump pytest from 7.4.0 to 7.4.1 (:pr:`2028`) :user:`dependabot`
#)  build(deps-dev): bump pre-commit from 3.3.3 to 3.4.0 (:pr:`2027`) :user:`dependabot`
#)  bdis_mac: Builds pass macOS notarization (:pr:`2025`) :user:`johan.ronnkvist`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2024`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pluggy from 1.2.0 to 1.3.0 (:pr:`2023`) :user:`dependabot`
#)  hooks: add pycryptodomex and update pycryptodome (:pr:`2022`) :user:`marcelotduarte`
#)  build-wheel: add support for ppc64le binary wheels for py310+ (:pr:`2020`) :user:`marcelotduarte`
#)  hooks: use module.exclude_names to filter missing modules (:pr:`2019`) :user:`marcelotduarte`
#)  hooks: improve tzdata/zoneinfo/pytz hooks a bit for use in zip (:pr:`2018`) :user:`marcelotduarte`
#)  build(deps-dev): bump wheel from 0.41.1 to 0.41.2 (:pr:`2017`) :user:`dependabot`
#)  doc: furo can be used only on html build (:pr:`2015`) :user:`marcelotduarte`
#)  build(deps-dev): update pre-commit and doc dependencies (:pr:`2014`) :user:`marcelotduarte`
#)  module: search for the stub file already parsed in the distribution (:pr:`2013`) :user:`marcelotduarte`
#)  hooks: qt extension modules are detected using stubs (:pr:`2009`) :user:`marcelotduarte`
#)  module: add a importshed for parsed stubs (:pr:`2008`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2007`) :user:`pre-commit-ci`
#)  module: get the implicit imports of extensions in a stub file (:pr:`2006`) :user:`marcelotduarte`
#)  module: propagate cache_path from the finder (:pr:`2005`) :user:`marcelotduarte`
#)  chore: new internal _typing module (:pr:`2004`) :user:`marcelotduarte`
#)  finder: cache_path holds where distribution data is saved (:pr:`2003`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.14.1 to 2.15.0 (:pr:`2002`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`2000`) :user:`pre-commit-ci`
#)  build(deps-dev): bump wheel from 0.41.0 to 0.41.1 (:pr:`1999`) :user:`dependabot`
#)  hooks: add markdown (:pr:`1997`) :user:`marcelotduarte`
#)  finder: improve scan code to detect packages using import call (:pr:`1966`) :user:`marcelotduarte`
#)  build(deps-dev): bump sphinx from 7.1.1 to 7.1.2 (:pr:`1995`) :user:`dependabot`
#)  module: ModuleHook class to support inheritance (:pr:`1998`) :user:`marcelotduarte`
#)  Bump version: 6.16.0-dev5 (:pr:`1994`) :user:`marcelotduarte`
#)  hooks: fix pyqt5 webengine [conda linux] (:pr:`1993`) :user:`marcelotduarte`
#)  hooks: fix pyside2 webengine [conda linux] (:pr:`1992`) :user:`marcelotduarte`
#)  samples: document the use of qt samples in conda-forge (:pr:`1991`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`1990`) :user:`pre-commit-ci`
#)  build(deps-dev): bump sphinx from 7.1.0 to 7.1.1 (:pr:`1989`) :user:`dependabot`
#)  hooks: move ssl hook to a submodule (:pr:`1988`) :user:`marcelotduarte`
#)  build(deps-dev): bump pylint from 2.17.4 to 2.17.5 (:pr:`1987`) :user:`dependabot`
#)  build(deps-dev): bump sphinx from 7.0.1 to 7.1.0 (:pr:`1985`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`1983`) :user:`pre-commit-ci`
#)  build(deps-dev): bump wheel from 0.40.0 to 0.41.0 (:pr:`1982`) :user:`dependabot`
#)  hooks: Disable sandbox in PySide2 WebEngine [Linux and Windows] (:pr:`1981`) :user:`marcelotduarte`
#)  hooks: Disable sandbox in PyQt5 WebEngine [Linux and Windows] (:pr:`1980`) :user:`marcelotduarte`
#)  hooks: support opencv-python 4.8.0 [msys2] (:pr:`1975`) :user:`marcelotduarte`
#)  hooks: support pyside6 6.5.1 [conda] (:pr:`1979`) :user:`marcelotduarte`
#)  hooks: support for pyqt6 6.5.1 [msys2] (:pr:`1977`) :user:`marcelotduarte`
#)  hooks: support pyside2 5.15.8 [msys2] (:pr:`1978`) :user:`marcelotduarte`
#)  hooks: fix for pyqt [conda linux] (:pr:`1976`) :user:`marcelotduarte`
#)  finder: add base modules at the end to simplify tests (:pr:`1974`) :user:`marcelotduarte`
#)  hooks: PySide2/6 - shiboken2/6 in zip_include_packages (:pr:`1970`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`1973`) :user:`pre-commit-ci`
#)  build-wheel: put jobs in concurrency for speedup [skip ci] (:pr:`1971`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.14.0 to 2.14.1 (:pr:`1972`) :user:`dependabot`
#)  startup: get rid of sysconfig at startup (:pr:`1968`) :user:`marcelotduarte`
#)  hooks: update sysconfig hook (:pr:`1967`) :user:`marcelotduarte`
#)  samples: update samples using wxPython (:pr:`1965`) :user:`marcelotduarte`
#)  hooks: multiprocessing support for forkserver and spawn (:pr:`1956`) :user:`marcelotduarte`
#)  hooks: add py-cord (fork of discord) (:pr:`1964`) :user:`marcelotduarte`
#)  tests: rewrite create_package to support dedent (:pr:`1960`) :user:`marcelotduarte`
#)  fix: bdist_rpm to pass tests in python 3.12b4 (:pr:`1963`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`1959`) :user:`pre-commit-ci`
#)  Bump version: 6.16.0-dev1 → 6.16.0-dev2 :user:`marcelotduarte`
#)  chore: enable Python 3.12 wheels and remove universal2 (:pr:`1958`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.13.1 to 2.14.0 (:pr:`1957`) :user:`dependabot`
#)  hooks: add boto3 (:pr:`1955`) :user:`marcelotduarte`
#)  hooks: move sklearn hook to a submodule (:pr:`1954`) :user:`marcelotduarte`
#)  hooks: fix the sentry_sdk hook (:pr:`1953`) :user:`marcelotduarte`
#)  hooks: improve hook for pillow [macos] (:pr:`1952`) :user:`marcelotduarte`
#)  fix: add rpath in macos executable [conda macos] (:pr:`1951`) :user:`marcelotduarte`
#)  samples: fix pydantic sample to work python < 3.10 (:pr:`1949`) :user:`marcelotduarte`
#)  chore: add more coverage reports [skip ci] (:pr:`1950`) :user:`marcelotduarte`
#)  fix: detection of dependent files and python shared library [conda linux/macos] (:pr:`1946`) :user:`marcelotduarte`
#)  fix: copy dependent files on "lib" directory [macOS] (:pr:`1942`) :user:`marcelotduarte`
#)  fix: support clang -fno-lto [conda macos] (:pr:`1948`) :user:`marcelotduarte`
#)  test: xfail some tests when rpmbuild is not present (:pr:`1947`) :user:`marcelotduarte`
#)  fix: bdist_rpm should generate only binaries [linux] (:pr:`1945`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pr:`1944`) :user:`pre-commit-ci`
#)  bases: update base executables and util module :user:`marcelotduarte`
#)  chore: more fine tuning pytest options [ci skip] (:pr:`1941`) :user:`marcelotduarte`
#)  tests: build executable to test in a subprocess (:pr:`1940`) :user:`marcelotduarte`
#)  chore: fine tuning pytest options (:pr:`1939`) :user:`marcelotduarte`
#)  chore: tweak to remove excess of pylint and noqa (:pr:`1938`) :user:`marcelotduarte`
#)  chore: add basic support for Python 3.12 (:pr:`1925`) :user:`marcelotduarte`
#)  parser: support for lief 0.14 ParserConfig (:pr:`1924`) :user:`marcelotduarte`
#)  chore: drop support for python 3.7 (:pr:`1935`) :user:`marcelotduarte`
#)  chore: to use pre-commit.ci add skip option (:pr:`1936`) :user:`marcelotduarte`
#)  Bump version: 6.16.0-dev0 → 6.16.0-dev1 (:pr:`1933`) :user:`marcelotduarte`
#)  chore: use pytest-xdist to speed up the tests (:pr:`1932`) :user:`marcelotduarte`
#)  fix: zip_include_packages/zip_exclude_packages regression (:pr:`1922`) :user:`marcelotduarte`
#)  build(deps-dev): bump ruff from 0.0.272 to 0.0.275 (:pr:`1930`) :user:`marcelotduarte`
#)  tests: add more test cases for ModuleFinder class (:pr:`1929`) :user:`marcelotduarte`
#)  tests: add more samples to tests (:pr:`1928`) :user:`marcelotduarte`
#)  chore: use pytest-datafiles to run tests in temporary path (:pr:`1927`) :user:`marcelotduarte`
#)  build(deps-dev): bump pytest from 7.3.2 to 7.4.0 (:pr:`1926`) :user:`dependabot`
#)  chore: cleanup tests and dependencies (:pr:`1923`) :user:`marcelotduarte`
#)  build(deps): update setuptools requirement from <68,>=62.6 to >=62.6,<69 (:pr:`1919`) :user:`dependabot`
#)  build(deps-dev): bump pytest-mock from 3.10.0 to 3.11.1 (:pr:`1918`) :user:`dependabot`
#)  chore: bump ruff 0.0.272 and fix local/system dependencies (:pr:`1914`) :user:`marcelotduarte`
#)  linux: bdist_rpm depends on rpmbuild being installed (:pr:`1913`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.13.0 to 2.13.1 (:pr:`1909`) :user:`dependabot`
#)  build(deps-dev): bump pytest from 7.3.1 to 7.3.2 (:pr:`1908`) :user:`dependabot`
#)  Bump version: 6.15.0 → 6.16.0-dev0 (:pr:`1905`) :user:`marcelotduarte`
#)  samples: add scipy sample (:pr:`1904`) :user:`marcelotduarte`
#)  hooks: fix scipy hooks used in zip_include_packages (:pr:`1903`) :user:`marcelotduarte`
#)  samples: update matplotlib sample using Wx (and remove deprecated test) (:pr:`1902`) :user:`marcelotduarte`
#)  samples: add a new matplotlib sample using Tk (:pr:`1901`) :user:`marcelotduarte`
#)  hooks: fix matplotlib hooks used in zip_include_packages (:pr:`1897`) :user:`marcelotduarte`
#)  hooks: improve scipy hooks (:pr:`1896`) :user:`marcelotduarte`
#)  fix: increase maximum recursion depth (:pr:`1890`) :user:`marcelotduarte`
#)  bases: update base executables and util module :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.12.3 to 2.13.0 (:pr:`1893`) :user:`dependabot`
#)  build(deps-dev): bump pytest-cov from 4.0.0 to 4.1.0 (:pr:`1891`) :user:`dependabot`
#)  Exit with non-zero exit code on exception (:pr:`1783`) :user:`johan.ronnkvist`
