7.x releases
############

Version 7.2 (Jul 16)
----------------------

#)  hooks: the optimized mode is the default for pip installations (:pull:`2500`) :user:`marcelotduarte`
#)  bdist_rpm: drop rpm2_mode and refactor spec_file (:pull:`2488`) :user:`marcelotduarte`
#)  bdist_appimage: remove zip file, propagate options, fixes docs (:pull:`2463`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.5.4 to 7.6.0 (:pull:`2498`) :user:`dependabot`
#)  bdist_msi: add license for msi (:pull:`2472`) :user:`nick`
#)  bdist_dmg: add dmgbuild as a dependency to improve mac dmg (:pull:`2442`) :user:`nick`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2494`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.24.1 to 0.24.2 (:pull:`2492`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.19.1 to 2.19.2 (:pull:`2491`) :user:`dependabot`
#)  tests: make test pass in conda-forge [osx, linux] (:pull:`2490`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2487`) :user:`pre-commit-ci`
#)  build(deps): bump sphinx-new-tab-link from 0.4.0 to 0.5.0 (:pull:`2486`) :user:`dependabot`
#)  exception: Only re-export setuptools errors to avoid exceptions not handled correctly (:pull:`2485`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.24.0 to 0.24.1 (:pull:`2484`) :user:`dependabot`
#)  hooks: add multiprocess (a multiprocessing fork) (:pull:`2475`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.23.0 to 0.24.0 (:pull:`2481`) :user:`dependabot`
#)  sample: add sample for Gtk (:pull:`2364`) :user:`cedk`
#)  chore: use setup-python-uv-action to cache uv packages (:pull:`2482`) :user:`marcelotduarte`
#)  tests: make tests pass on mingw (:pull:`2476 regression) (#2480`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2479`) :user:`pre-commit-ci`
#)  build(deps): bump coverage from 7.5.3 to 7.5.4 (:pull:`2477`) :user:`dependabot`
#)  tests: improve _compat to use in tests (:pull:`2476`) :user:`marcelotduarte`
#)  tests: fix test_cli in archlinux (:pull:`2470`) :user:`marcelotduarte`
#)  build(deps): bump update setuptools requirement to >=65.6.3,<71 (:pull:`2468`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2464`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.22.0 to 0.23.0 (:pull:`2462`) :user:`dependabot`
#)  hooks: support numpy 2.0 (:pull:`2466`) :user:`marcelotduarte`
#)  Bump version: 7.1.0-post0 → 7.1.1 [ci skip] (:pull:`2461`) :user:`marcelotduarte`
#)  hooks: improve scikit-image (:pull:`2460`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.19.0 to 2.19.1 (:pull:`2458`) :user:`dependabot`
#)  hooks: add rasterio (:pull:`2455`) :user:`marcelotduarte`
#)  hooks: fix #2382 regression / improve tests and docs (:pull:`2443`) :user:`marcelotduarte`
#)  hooks: avoid exception when distribution is none (:pull:`2452`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.21.1 to 0.22.0 (:pull:`2450`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2448`) :user:`pre-commit-ci`
#)  build(deps-dev): bump cibuildwheel from 2.18.1 to 2.19.0 (:pull:`2447`) :user:`dependabot`
#)  doc: small revision of development/index [ci skip] (:pull:`2446`) :user:`marcelotduarte`
#)  bdist_rpm: Fix string concat error due to order of op for + and or in RPM (:pull:`2444`) :user:`nicktindle`
#)  cli: fix sys.path for cxfreeze command line (:pull:`2439`) :user:`marcelotduarte`
#)  build(deps): bump pytest from 8.2.1 to 8.2.2 (:pull:`2437`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2434`) :user:`pre-commit-ci`
#)  Bump version: 7.1.0 → 7.1.0-post0 [ci skip] (:pull:`2432`) :user:`marcelotduarte`
#)  doc: msvc faq revision [ci skip] (:pull:`2429`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.5.2 to 7.5.3 (:pull:`2428`) :user:`dependabot`
#)  hooks: fix pygobject hook for Linux (:pull:`2425`) :user:`marcelotduarte`

Version 7.1 (May 26)
----------------------

#)  hooks: add mkl (:pull:`2420`) :user:`marcelotduarte`
#)  hooks: resolve dependencies to avoid symlink in numpy/mkl/blas conda linux (:pull:`2419`) :user:`marcelotduarte`
#)  module: fix distribuition installer multiline (:pull:`2418`) :user:`marcelotduarte`
#)  ci: add test to do more 'parser' and 'module' coverage (:pull:`2416`) :user:`marcelotduarte`
#)  freezer: resolve symlinks to always copy the source (:pull:`2415`) :user:`marcelotduarte`
#)  build(deps): update setuptools requirement from <70,>=62.6 to >=62.6,<71 (:pull:`2413`) :user:`dependabot`
#)  freezer: resolve dependencies to avoid symlink [linux] (:pull:`2410`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2409`) :user:`pre-commit-ci`
#)  build(deps-dev): bump cibuildwheel from 2.18.0 to 2.18.1 (:pull:`2408`) :user:`dependabot`
#)  build(deps): bump pytest from 8.2.0 to 8.2.1 (:pull:`2407`) :user:`dependabot`
#)  hooks: support for numpy + oneMKL using pip windows (:pull:`2405`) :user:`marcelotduarte`
#)  hooks: support for numpy+mkl on conda linux (:pull:`2404`) :user:`marcelotduarte`
#)  module: improve version method and add new methods (:pull:`2403`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.21.0 to 0.21.1 (:pull:`2399`) :user:`dependabot`
#)  bdist_deb: catch a cpio 2.13 bug (:pull:`2402`) :user:`marcelotduarte`
#)  chore: use uv pip to make installing packages faster (:pull:`2397`) :user:`marcelotduarte`
#)  tests: xfail bdist_dmg when "Resource busy" [macOS] (:pull:`2396`) :user:`marcelotduarte`
#)  doc: use uv pip (:pull:`2395`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2394`) :user:`pre-commit-ci`
#)  build(deps-dev): bump cibuildwheel from 2.17.0 to 2.18.0 (:pull:`2393`) :user:`dependabot`
#)  hooks: add wayland Qt plugins automatically (:pull:`2391`) :user:`marcelotduarte`
#)  hooks: add missing Qt plugins and translations (:pull:`2390`) :user:`marcelotduarte`
#)  hooks: update plugins and translations for qt 6.7 (:pull:`2389`) :user:`marcelotduarte`
#)  doc: add faq 'Removing the MAX_PATH Limitation' (:pull:`2388`) :user:`marcelotduarte`
#)  chore: use compile() with dont_inherit and optimize (:pull:`2387`) :user:`marcelotduarte`
#)  hooks: additional translations to qt hooks (:pull:`2386`) :user:`marcelotduarte`
#)  fix: global of main module to work better with multiprocessing (:pull:`2385`) :user:`marcelotduarte`
#)  hooks: improve multiprocessing hook to work with pytorch (:pull:`2382`) :user:`marcelotduarte`
#)  build_exe: add new option --zip-filename (:pull:`2379`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2381`) :user:`pre-commit-ci`
#)  build(deps): bump coverage from 7.5.0 to 7.5.1 (:pull:`2380`) :user:`dependabot`
#)  build-wheel: reactivate universal2 wheels for macOS (:pull:`2378`) :user:`marcelotduarte`
#)  hooks: add pygobject (:pull:`2375`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.20.3 to 0.21.0 (:pull:`2377`) :user:`dependabot`
#)  build(deps): bump pytest-xdist[psutil] from 3.5.0 to 3.6.1 (:pull:`2370`) :user:`dependabot`
#)  build(deps): bump pytest from 8.1.2 to 8.2.0 (:pull:`2372`) :user:`dependabot`
#)  build(deps): bump myst-parser from 3.0.0 to 3.0.1 (:pull:`2371`) :user:`dependabot`
#)  samples: adapt code to support ruff rules (:pull:`2369`) :user:`marcelotduarte`
#)  build(deps-dev): update pytest to 8.1.2, revert pyetst-xdist to 3.5.0 (:pull:`2368`) :user:`marcelotduarte`
#)  tests: make msys2/mingw tests pass (:pull:`2367`) :user:`marcelotduarte`
#)  bdist_msi: ignore warning 'msilib' is deprecated (:pull:`2366`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.20.2 to 0.20.3 (:pull:`2365`) :user:`dependabot`
#)  hooks: fix unbound variable in load_subprocess under MINGW (:pull:`2363`) :user:`cedk`
#)  ci: try to catch a issue with macos (:pull:`2360`) :user:`marcelotduarte`
#)  hooks: Recompile the numpy.core.overrides module to limit optimization (:pull:`2358`) :user:`marcelotduarte`
#)  hooks: fix regression in msys2 (:pull:`2357`) :user:`marcelotduarte`
#)  build(deps): bump coverage from 7.4.4 to 7.5.0 (:pull:`2355`) :user:`dependabot`
#)  ci: CI tests fails using macos-latest (:pull:`2359`) :user:`marcelotduarte`
#)  tests: add command line tests for build_exe (:pull:`2353`) :user:`marcelotduarte`
#)  build(deps): bump myst-parser from 2.0.0 to 3.0.0 (:pull:`2351`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.20.1 to 0.20.2 (:pull:`2350`) :user:`dependabot`
#)  tests: xfail bdist_dmg if resource is busy (:pull:`2352`) :user:`marcelotduarte`
#)  build(deps): bump pluggy from 1.4.0 to 1.5.0 (:pull:`2348`) :user:`dependabot`
#)  Bump version: 7.0.0 → 7.1.0-dev0 [ci skip] (:pull:`2349`) :user:`marcelotduarte`

Version 7.0 (April 21)
----------------------

#)  hooks: support numpy in python 3.12 (:pull:`2345`) :user:`marcelotduarte`
#)  test: add simple test for bdist_mac (:pull:`2343`) :user:`marcelotduarte`
#)  fix: regression in _pre_copy_hook (Linux) (:pull:`2342`) :user:`marcelotduarte`
#)  build(deps): update dev dependencies (:pull:`2341`) :user:`marcelotduarte`
#)  parser: show what patchelf is doing if silent is off (:pull:`2340`) :user:`marcelotduarte`
#)  initscripts: use of __loader__ is deprecated (:pull:`2338`) :user:`marcelotduarte`
#)  tests: add test_hooks_pandas.py (:pull:`2336`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.20.0 to 0.20.1 (:pull:`2337`) :user:`dependabot`
#)  test: an expected exception should not be treated as an expected failure (:pull:`2334`) :user:`marcelotduarte`
#)  fix: coverage report usage and omit option (:pull:`2333`) :user:`marcelotduarte`
#)  test: add a linux binary wheel test in ci (:pull:`2332`) :user:`marcelotduarte`
#)  chore: generate multiple files for requirements (:pull:`2330`) :user:`marcelotduarte`
#)  doc: Correct some typographical errors and grammar errors (:pull:`2328`) :user:`marcelotduarte`
#)  doc: show builtdist command as toctree and clickable in the table (:pull:`2327`) :user:`marcelotduarte`
#)  doc: separates bdist commands to nest them in builtdist (:pull:`2325`) :user:`marcelotduarte`
#)  doc: show pyproject.toml as fisrt example (:pull:`2326`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2324`) :user:`pre-commit-ci`
#)  chore: move License to the project root dir (:pull:`2323`) :user:`marcelotduarte`
#)  doc: fix furo edit button [ci skip] (:pull:`2322`) :user:`marcelotduarte`
#)  docs: add 'Creating Built Distributions' (:pull:`2321`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.19.3 to 0.20.0 (:pull:`2320`) :user:`dependabot`
#)  chore: refactor internal modules (:pull:`2319`) :user:`marcelotduarte`
#)  build(deps): pin dev dependencies (:pull:`2318`) :user:`marcelotduarte`
#)  bases: update base executables and util module [ci skip] (:pull:`2317`) :user:`marcelotduarte`
#)  chore: remove deprecated option in 'build' command (:pull:`2316`) :user:`marcelotduarte`
#)  Bump version: 6.16.0-dev12 → 7.0.0-rc0 [ci skip] (:pull:`2315`) :user:`marcelotduarte`
#)  chore: remove unused class (:pull:`2314`) :user:`marcelotduarte`
#)  build(deps-dev): bump pytest-mock from 3.12.0 to 3.14.0 (:pull:`2311`) :user:`dependabot`
#)  tests: add TYPE_CHECKING to coverage excludes (:pull:`2310`) :user:`marcelotduarte`
#)  chore: improve annotation (using ruff to check) (:pull:`2309`) :user:`marcelotduarte`
#)  chore: adapt code to support ruff 'S' rules (:pull:`2308`) :user:`marcelotduarte`
#)  chore: improve type checking (w/ help of ruff) (:pull:`2307`) :user:`marcelotduarte`
#)  build(deps-dev): bump sphinx-new-tab-link from 0.3.1 to 0.4.0 (:pull:`2306`) :user:`dependabot`
#)  chore: use more ruff lint rules (:pull:`2305`) :user:`marcelotduarte`
#)  chore: enable ruff 'EM' ruleset (:pull:`2304`) :user:`marcelotduarte`
#)  build: fix for Python 3.12 Ubuntu Linux 24.04 (Noble Nimbat) (:pull:`2303`) :user:`marcelotduarte`
#)  hooks: support tensorflow plugins (:pull:`2302`) :user:`marcelotduarte`
#)  hooks: add easyocr and torchvision (also update skickit-image and pytorch) (:pull:`2286`) :user:`marcelotduarte`
#)  build(deps-dev): bump coverage from 7.4.3 to 7.4.4 (:pull:`2301`) :user:`dependabot`
#)  build-wheel: use macos-14 (native arm) with cibuildwheel (:pull:`2299`) :user:`marcelotduarte`
#)  build(deps): update wheel requirement from <=0.42.0,>=0.38.4 to >=0.38.4,<=0.43.0 (:pull:`2298`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.16.5 to 2.17.0 (:pull:`2297`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.18.3 to 0.19.0 (:pull:`2296`) :user:`dependabot`
#)  cli: restore more deprecated options (:pull:`2295`) :user:`marcelotduarte`
#)  build(deps-dev): bump ruff-pre-commit 0.3.2 [ci skip] (:pull:`2294`) :user:`marcelotduarte`
#)  build(deps-dev): bump sphinx-new-tab-link from 0.3.0 to 0.3.1 (:pull:`2292`) :user:`dependabot`
#)  build(deps-dev): bump pytest from 8.0.2 to 8.1.1 (:pull:`2291`) :user:`dependabot`
#)  build(deps-dev): bump pytest-timeout from 2.2.0 to 2.3.1 (:pull:`2289`) :user:`dependabot`
#)  doc: improve the code_layout a bit (:pull:`2288`) :user:`marcelotduarte`
#)  hooks: support pytorch 2.2 (:pull:`2281`) :user:`marcelotduarte`
#)  docs: update msvcr links (:pull:`2284`) :user:`marcelotduarte`
#)  build(deps-dev): bump sphinx-new-tab-link from 0.2.3 to 0.3.0 (:pull:`2282`) :user:`dependabot`
#)  build(deps-dev): bump sphinx-new-tab-link from 0.2.2 to 0.2.3 (:pull:`2279`) :user:`dependabot`
#)  build(deps-dev): bump coverage from 7.4.2 to 7.4.3 (:pull:`2278`) :user:`dependabot`
#)  build(deps-dev): bump pytest from 8.0.1 to 8.0.2 (:pull:`2277`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.17.4 to 0.18.3 (:pull:`2276`) :user:`dependabot`
#)  bdist_msi: remove unused code (:pull:`2270`) :user:`marcelotduarte`
#)  build(deps-dev): bump coverage from 7.4.1 to 7.4.2 (:pull:`2271`) :user:`dependabot`
#)  tests: improve bdist_msi tests and samples (:pull:`2269`) :user:`marcelotduarte`
#)  chore: use only 'ruff' as a linter and formatter (:pull:`2268`) :user:`marcelotduarte`
#)  build(deps): support lief 0.14.x (:pull:`2267`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2266`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pytest from 8.0.0 to 8.0.1 (:pull:`2265`) :user:`dependabot`
#)  freezer: remove dead code (not used in py38+) (:pull:`2263`) :user:`marcelotduarte`
#)  tests: improve a bit build_exe and freezer tests (:pull:`2262`) :user:`marcelotduarte`
#)  bdist_deb: fix call to bdist_rpm, improve tests (:pull:`2260`) :user:`marcelotduarte`
#)  pre-commit: use validate-pyproject-schema-store (:pull:`2258`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2257`) :user:`pre-commit-ci`
#)  build(deps-dev): bump furo from 2023.9.10 to 2024.1.29 (:pull:`2256`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.17.3 to 0.17.4 (:pull:`2255`) :user:`dependabot`
#)  tests: add more tests for freezer (:pull:`2254`) :user:`marcelotduarte`
#)  build-exe: adds include_path option (formerly in cli) (:pull:`2253`) :user:`marcelotduarte`
#)  fix: #2242 introduced a regression in install_exe (:pull:`2250`) :user:`marcelotduarte`
#)  fix: remove misuse of packages in setuptools.setup (:pull:`2249`) :user:`marcelotduarte`
#)  tests: add more tests for bdist_msi (:pull:`2248`) :user:`marcelotduarte`
#)  chore: add support for pyproject.toml (tool.cxfreeze) (:pull:`2244`) :user:`marcelotduarte`
#)  build(deps): bump codecov/codecov-action from 3 to 4 (:pull:`2238`) :user:`dependabot`
#)  build(deps-dev): bump sphinx-new-tab-link from 0.2.1 to 0.2.2 (:pull:`2245`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2243`) :user:`pre-commit-ci`
#)  fix: incorrect metadata usage in install/install_exe (:pull:`2242`) :user:`marcelotduarte`
#)  tests: improve coverage tests for linux (:pull:`2241`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.16.4 to 2.16.5 (:pull:`2237`) :user:`dependabot`
#)  ci: add specific coverage test for linux (:pull:`2239`) :user:`marcelotduarte`
#)  fix: coverage report extra tests (:pull:`2236`) :user:`marcelotduarte`
#)  chore: rearranges and sort some settings (:pull:`2235`) :user:`marcelotduarte`
#)  chore: improve the use of coverage (:pull:`2233`) :user:`marcelotduarte`
#)  build(deps-dev): bump black 2024 (:pull:`2230`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.16.2 to 2.16.4 (:pull:`2229`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.17.1 to 0.17.3 (:pull:`2228`) :user:`dependabot`
#)  build(deps-dev): bump pytest from 7.4.4 to 8.0.0 (:pull:`2227`) :user:`dependabot`
#)  tests: add some freezer tests (:pull:`2226`) :user:`marcelotduarte`
#)  executable: new option --uac-uiaccess (:pull:`2135`) :user:`marcelotduarte`
#)  chore: add options to pre-commit (:pull:`2225`) :user:`marcelotduarte`
#)  tests: test build_exe options silent,silent-level and build_exe (:pull:`2224`) :user:`marcelotduarte`
#)  tests: target_dir "starts in a clean directory" (:pull:`2223`) :user:`marcelotduarte`
#)  build(deps-dev): bump bump-my-version from 0.17.0 to 0.17.1 (:pull:`2222`) :user:`dependabot`
#)  winversioninfo: comments length must be limited to fit WORD (:pull:`2220`) :user:`marcelotduarte`
#)  tests: add tests for __main__ and cli (:pull:`2219`) :user:`marcelotduarte`
#)  build(deps-dev): bump pluggy from 1.3.0 to 1.4.0 (:pull:`2217`) :user:`dependabot`
#)  parser: minor fix to support lief 0.14 (:pull:`2216`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2215`) :user:`pre-commit-ci`
#)  build(deps-dev): bump sphinx-tabs from 3.4.4 to 3.4.5 (:pull:`2214`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.16.2 to 0.17.0 (:pull:`2213`) :user:`dependabot`
#)  winversioninfo: fix version string and improve coverage/tests (:pull:`2211`) :user:`marcelotduarte`
#)  chore: Update copyright year and license (:pull:`2209`) :user:`marcelotduarte`
#)  docs: open extenal links in new tab (:pull:`2208`) :user:`marcelotduarte`
#)  hooks: add pyproj (:pull:`2207`) :user:`marcelotduarte`
#)  winmsvcr: extend support for VS 2022 (:pull:`2204`) :user:`marcelotduarte`
#)  hooks: opencv-python - minor fixes (:pull:`2206`) :user:`marcelotduarte`
#)  freezer: improve/fixes validate_executable (:pull:`2205`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2202`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.16.1 to 0.16.2 (:pull:`2201`) :user:`dependabot`
#)  tests: minor tweaks - part 2 (:pull:`2198`) :user:`marcelotduarte`
#)  tests: minor tweaks - part 1 (:pull:`2197`) :user:`marcelotduarte`
#)  build(deps-dev): bump pre-commit up to 3.6.0 and sphinx up to 7.2.6 (:pull:`2196`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2195`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.16.0 to 0.16.1 (:pull:`2194`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.15.4 to 0.16.0 (:pull:`2191`) :user:`dependabot`
#)  tests: simplify more tests using run_command (:pull:`2189`) :user:`marcelotduarte`
#)  tests: simplify test using a run_command (:pull:`2187`) :user:`marcelotduarte`
#)  build(deps-dev): bump pytest from 7.4.3 to 7.4.4 (:pull:`2188`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.15.3 to 0.15.4 (:pull:`2186`) :user:`dependabot`
#)  setup script: add an extension to executable icon that is valid across OS (:pull:`2185`) :user:`marcelotduarte`
#)  setup script: pre-defined values for base are valid in all OS (:pull:`2184`) :user:`marcelotduarte`
#)  setup script: extend executables keyword to support more types (:pull:`2182`) :user:`marcelotduarte`
#)  bdist_appimage: build Linux AppImage format [new feature] (:pull:`2050`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2181`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.15.1 to 0.15.3 (:pull:`2178`) :user:`dependabot`
#)  build-wheel: fix update_bases' ref and cleanup publish (:pull:`2176`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2175`) :user:`pre-commit-ci`
#)  build(deps-dev): bump bump-my-version from 0.12.0 to 0.15.1 (:pull:`2174`) :user:`dependabot`
#)  Bump version: 6.16.0-dev11 → 6.16.0-dev12 [ci skip] (:pull:`2173`) :user:`marcelotduarte`
#)  bdist_mac: create symlink between folders specified by user under Resources (:pull:`2169`) :user:`admin`
#)  fix: #2139 introduced a regression [macos] (:pull:`2172`) :user:`marcelotduarte`
#)  hooks: add AV and PyAV (:pull:`2165`) :user:`marcelotduarte`
#)  build: fix build_wheel (after #2162 and #2163) (:pull:`2170`) :user:`marcelotduarte`
#)  build(deps): bump actions/download-artifact from 3 to 4 (:pull:`2163`) :user:`dependabot`
#)  build(deps): bump actions/upload-artifact from 3 to 4 (:pull:`2162`) :user:`dependabot`
#)  build(deps): bump github/codeql-action from 2 to 3 (:pull:`2160`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2157`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pylint from 3.0.2 to 3.0.3 (:pull:`2156`) :user:`dependabot`
#)  build(deps): bump actions/setup-python from 4 to 5 (:pull:`2155`) :user:`dependabot`
#)  Replace SetDllDirectory by AddDllDirectory (:pull:`2144`) :user:`dev`
#)  Bump version: 6.16.0-dev10 → 6.16.0-dev11 [ci skip] (:pull:`2151`) :user:`marcelotduarte`
#)  fix: pthread missing for building in FreeBSD (:pull:`2150`) :user:`marcelotduarte`
#)  build(deps): bump wheel from 0.41.3 to 0.42.0 (:pull:`2148`) :user:`dependabot`
#)  build(deps-dev): bump bump-my-version from 0.11.0 to 0.12.0 (:pull:`2147`) :user:`dependabot`
#)  chore: switch to bump-my-version (:pull:`2146`) :user:`marcelotduarte`
#)  bdist_mac: apply the style of other bdist modules (:pull:`2139`) :user:`marcelotduarte`
#)  hooks: add yt_dlp (:pull:`2145`) :user:`marcelotduarte`
#)  build(deps-dev): bump pytest-xdist[psutil] from 3.4.0 to 3.5.0 (:pull:`2143`) :user:`dependabot`
#)  build(deps): update setuptools requirement from <69,>=62.6 to >=62.6,<70 (:pull:`2141`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2142`) :user:`pre-commit-ci`
#)  freezer: Improve symlink support to work w/ macOS (:pull:`2138`) :user:`marcelotduarte`
#)  hooks: adds anyio, pyarrow and tiktoken (:pull:`2134`) :user:`marcelotduarte`
#)  chore: cosmetic and minor tweaks (:pull:`2137`) :user:`marcelotduarte`
#)  build_exe: raise exception on invalid build_exe option (:pull:`2132`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2130`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pytest-xdist[psutil] from 3.3.1 to 3.4.0 (:pull:`2129`) :user:`dependabot`
#)  samples: improve qt samples (:pull:`2128`) :user:`marcelotduarte`
#)  hooks: Support for PyQt5/PySide2 QtWebEngine in macOS (:pull:`2127`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2125`) :user:`pre-commit-ci`
#)  hooks: Support for PyQt6/PySide6 QtWebEngine in macOS (:pull:`2124`) :user:`marcelotduarte`
#)  hooks: use a different approach for pyqt6 in bdist_mac (:pull:`2123`) :user:`marcelotduarte`
#)  hooks: fix pyqt6 in bdist_mac (.app) (:pull:`2122`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2120`) :user:`pre-commit-ci`
#)  build(deps): bump wheel from 0.41.2 to 0.41.3 (:pull:`2119`) :user:`dependabot`
#)  build(deps-dev): bump pytest from 7.4.2 to 7.4.3 (:pull:`2115`) :user:`dependabot`
#)  "Bump version: 6.16.0-dev9 → 6.16.0-dev10 [ci skip]" (:pull:`2114`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2113`) :user:`pre-commit-ci`
#)  build(deps-dev): bump sphinx-tabs from 3.4.1 to 3.4.4 (:pull:`2112`) :user:`dependabot`
#)  build(deps-dev): bump pylint from 3.0.1 to 3.0.2 (:pull:`2111`) :user:`dependabot`
#)  hooks: fix qtwebengine in conda-forge (:pull:`2110`) :user:`marcelotduarte`
#)  hooks: fix qt.conf for pyqt [macos] (:pull:`2109`) :user:`marcelotduarte`
#)  hooks: tweaks to the debugging of qt hooks (:pull:`2108`) :user:`marcelotduarte`
#)  bdist_mac: move set_relative_reference_paths to build_exe (:pull:`2106`) :user:`marcelotduarte`
#)  darwintools: fix adhocsignature for universal2 machine (:pull:`2107`) :user:`marcelotduarte`
#)  bdist_mac: make symlink between Resources/share and Contents/MacOS (:pull:`2105`) :user:`marcelotduarte`
#)  parse: regression fix in get_dependent_files [windows] (:pull:`2104`) :user:`marcelotduarte`
#)  bdist_mac: skip text files in set_relative_reference_paths (:pull:`2102`) :user:`micah`
#)  build(deps-dev): bump pytest-mock from 3.11.1 to 3.12.0 (:pull:`2103`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2101`) :user:`pre-commit-ci`
#)  bases: update base executables and util module [ci skip] (:pull:`2100`) :user:`marcelotduarte`
#)  chore: update base executables and util module [ci skip] (:pull:`2099`) :user:`marcelotduarte`
#)  "Bump version: 6.16.0-dev8 → 6.16.0-dev9 [ci skip]" (:pull:`2098`) :user:`marcelotduarte`
#)  fix: issues with manifest and windows version (:pull:`2097`) :user:`marcelotduarte`
#)  build(deps-dev): bump pre-commit from 3.4.0 to 3.5.0 (:pull:`2096`) :user:`dependabot`
#)  hooks: add triton and support for pytorch 2.1 (:pull:`2090`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2092`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pytest-timeout from 2.1.0 to 2.2.0 (:pull:`2091`) :user:`dependabot`
#)  build(deps-dev): bump pylint from 3.0.0 to 3.0.1 (:pull:`2089`) :user:`dependabot`
#)  build(deps-dev): bump cibuildwheel from 2.16.1 to 2.16.2 (:pull:`2085`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2082`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pylint from 2.17.6 to 3.0.0 (:pull:`2081`) :user:`dependabot`
#)  tests: use importorskip/skip at module level to skip early (:pull:`2084`) :user:`marcelotduarte`
#)  chore: rewrite some imports as absolute (:pull:`2083`) :user:`marcelotduarte`
#)  bdist_deb: add doc and tests (:pull:`2080`) :user:`marcelotduarte`
#)  doc: minor fixes (:pull:`2079`) :user:`marcelotduarte`
#)  bdist_deb: create an DEB distribution [new feature] (:pull:`2078`) :user:`marcelotduarte`
#)  bdist_rpm: remove unused options (:pull:`2077`) :user:`marcelotduarte`
#)  "Bump version: 6.16.0-dev7 → 6.16.0-dev8 [ci skip]" (:pull:`2076`) :user:`marcelotduarte`
#)  bdist_rpm: fix issue with install prefix (:pull:`2075`) :user:`marcelotduarte`
#)  hooks: initialize blas [numpy conda-forge] (:pull:`2074`) :user:`49456524+IperGiove`
#)  parser: exclude LD_PRELOAD to not include triggered dependencies (:pull:`2073`) :user:`marcelotduarte`
#)  hooks: add tidylib (:pull:`2072`) :user:`marcelotduarte`
#)  parser: use the internal path instead of sys.path (:pull:`2071`) :user:`marcelotduarte`
#)  fix: avoid false builtin modules developing in multi-environment (:pull:`2070`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.16.0 to 2.16.1 (:pull:`2069`) :user:`dependabot`
#)  hooks: move tkinter and tz data to share folder (:pull:`2067`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2066`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pylint from 2.17.5 to 2.17.6 (:pull:`2065`) :user:`dependabot`
#)  tests: minor tweaks (:pull:`2063`) :user:`marcelotduarte`
#)  build_exe: fix typo in command line boolean option 'include-msvcr' (:pull:`2062`) :user:`marcelotduarte`
#)  hooks: fix scipy windows (:pull:`2060`) :user:`marcelotduarte`
#)  doc: improve documentation for 'binary wheels' (:pull:`2059`) :user:`marcelotduarte`
#)  hooks: add numpy 1.26 (:pull:`2058`) :user:`marcelotduarte`
#)  hooks: fix numpy/scipy regression [mingw] (:pull:`2057`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.15.0 to 2.16.0 (:pull:`2056`) :user:`dependabot`
#)  hooks: add RNS (Reticulum) (:pull:`2053`) :user:`marcelotduarte`
#)  bdist_mac: Copy build_exe to Resources and move executables to MacOS (:pull:`2048`) :user:`marcelotduarte`
#)  hooks: fix numpy/scipy dylibs are included twice (:pull:`2038`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2055`) :user:`pre-commit-ci`
#)  "Bump version: 6.16.0-dev6 → 6.16.0-dev7 [ci skip]" (:pull:`2052`) :user:`marcelotduarte`
#)  icons: add Python icons (:pull:`2051`) :user:`marcelotduarte`
#)  Revert "build(deps): bump codecov/codecov-action from 3 to 4" (:pull:`2049`) :user:`marcelotduarte`
#)  build(deps): bump codecov/codecov-action from 3 to 4 (:pull:`2047`) :user:`dependabot`
#)  samples: small tweaks to demonstrate independent options (:pull:`2045`) :user:`marcelotduarte`
#)  build(deps): bump docker/setup-qemu-action from 2 to 3 (:pull:`2044`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2043`) :user:`pre-commit-ci`
#)  bdist_mac: small optimization on copy tree (:pull:`2040`) :user:`marcelotduarte`
#)  bdist_mac: fix duplicate lib in bdist_dmg [regression] (:pull:`2037`) :user:`marcelotduarte`
#)  hooks: improve numpy and pandas hooks (:pull:`2036`) :user:`marcelotduarte`
#)  build(deps-dev): bump pytest from 7.4.1 to 7.4.2 (:pull:`2035`) :user:`dependabot`
#)  "Bump version: 6.16.0-dev5 → 6.16.0-dev6 [ci skip]" (:pull:`2034`) :user:`marcelotduarte`
#)  doc: Building binary wheels (:pull:`2033`) :user:`marcelotduarte`
#)  hooks: add support for pandas 2.1.0 (:pull:`2032`) :user:`marcelotduarte`
#)  build-wheel: fix build and compatibility w/ build 1.0 (:pull:`2030`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2031`) :user:`pre-commit-ci`
#)  build(deps): bump actions/checkout from 3 to 4 (:pull:`2029`) :user:`dependabot`
#)  build(deps-dev): bump pytest from 7.4.0 to 7.4.1 (:pull:`2028`) :user:`dependabot`
#)  build(deps-dev): bump pre-commit from 3.3.3 to 3.4.0 (:pull:`2027`) :user:`dependabot`
#)  bdis_mac: Builds pass macOS notarization (:pull:`2025`) :user:`johan.ronnkvist`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2024`) :user:`pre-commit-ci`
#)  build(deps-dev): bump pluggy from 1.2.0 to 1.3.0 (:pull:`2023`) :user:`dependabot`
#)  hooks: add pycryptodomex and update pycryptodome (:pull:`2022`) :user:`marcelotduarte`
#)  build-wheel: add support for ppc64le binary wheels for py310+ (:pull:`2020`) :user:`marcelotduarte`
#)  hooks: use module.exclude_names to filter missing modules (:pull:`2019`) :user:`marcelotduarte`
#)  hooks: improve tzdata/zoneinfo/pytz hooks a bit for use in zip (:pull:`2018`) :user:`marcelotduarte`
#)  build(deps-dev): bump wheel from 0.41.1 to 0.41.2 (:pull:`2017`) :user:`dependabot`
#)  doc: furo can be used only on html build (:pull:`2015`) :user:`marcelotduarte`
#)  build(deps-dev): update pre-commit and doc dependencies (:pull:`2014`) :user:`marcelotduarte`
#)  module: search for the stub file already parsed in the distribution (:pull:`2013`) :user:`marcelotduarte`
#)  hooks: qt extension modules are detected using stubs (:pull:`2009`) :user:`marcelotduarte`
#)  module: add a importshed for parsed stubs (:pull:`2008`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2007`) :user:`pre-commit-ci`
#)  module: get the implicit imports of extensions in a stub file (:pull:`2006`) :user:`marcelotduarte`
#)  module: propagate cache_path from the finder (:pull:`2005`) :user:`marcelotduarte`
#)  chore: new internal _typing module (:pull:`2004`) :user:`marcelotduarte`
#)  finder: cache_path holds where distribution data is saved (:pull:`2003`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.14.1 to 2.15.0 (:pull:`2002`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`2000`) :user:`pre-commit-ci`
#)  build(deps-dev): bump wheel from 0.41.0 to 0.41.1 (:pull:`1999`) :user:`dependabot`
#)  hooks: add markdown (:pull:`1997`) :user:`marcelotduarte`
#)  finder: improve scan code to detect packages using import call (:pull:`1966`) :user:`marcelotduarte`
#)  build(deps-dev): bump sphinx from 7.1.1 to 7.1.2 (:pull:`1995`) :user:`dependabot`
#)  module: ModuleHook class to support inheritance (:pull:`1998`) :user:`marcelotduarte`
#)  Bump version: 6.16.0-dev5 (:pull:`1994`) :user:`marcelotduarte`
#)  hooks: fix pyqt5 webengine [conda linux] (:pull:`1993`) :user:`marcelotduarte`
#)  hooks: fix pyside2 webengine [conda linux] (:pull:`1992`) :user:`marcelotduarte`
#)  samples: document the use of qt samples in conda-forge (:pull:`1991`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`1990`) :user:`pre-commit-ci`
#)  build(deps-dev): bump sphinx from 7.1.0 to 7.1.1 (:pull:`1989`) :user:`dependabot`
#)  hooks: move ssl hook to a submodule (:pull:`1988`) :user:`marcelotduarte`
#)  build(deps-dev): bump pylint from 2.17.4 to 2.17.5 (:pull:`1987`) :user:`dependabot`
#)  build(deps-dev): bump sphinx from 7.0.1 to 7.1.0 (:pull:`1985`) :user:`dependabot`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`1983`) :user:`pre-commit-ci`
#)  build(deps-dev): bump wheel from 0.40.0 to 0.41.0 (:pull:`1982`) :user:`dependabot`
#)  hooks: Disable sandbox in PySide2 WebEngine [Linux and Windows] (:pull:`1981`) :user:`marcelotduarte`
#)  hooks: Disable sandbox in PyQt5 WebEngine [Linux and Windows] (:pull:`1980`) :user:`marcelotduarte`
#)  hooks: support opencv-python 4.8.0 [msys2] (:pull:`1975`) :user:`marcelotduarte`
#)  hooks: support pyside6 6.5.1 [conda] (:pull:`1979`) :user:`marcelotduarte`
#)  hooks: support for pyqt6 6.5.1 [msys2] (:pull:`1977`) :user:`marcelotduarte`
#)  hooks: support pyside2 5.15.8 [msys2] (:pull:`1978`) :user:`marcelotduarte`
#)  hooks: fix for pyqt [conda linux] (:pull:`1976`) :user:`marcelotduarte`
#)  finder: add base modules at the end to simplify tests (:pull:`1974`) :user:`marcelotduarte`
#)  hooks: PySide2/6 - shiboken2/6 in zip_include_packages (:pull:`1970`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`1973`) :user:`pre-commit-ci`
#)  build-wheel: put jobs in concurrency for speedup [skip ci] (:pull:`1971`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.14.0 to 2.14.1 (:pull:`1972`) :user:`dependabot`
#)  startup: get rid of sysconfig at startup (:pull:`1968`) :user:`marcelotduarte`
#)  hooks: update sysconfig hook (:pull:`1967`) :user:`marcelotduarte`
#)  samples: update samples using wxPython (:pull:`1965`) :user:`marcelotduarte`
#)  hooks: multiprocessing support for forkserver and spawn (:pull:`1956`) :user:`marcelotduarte`
#)  hooks: add py-cord (fork of discord) (:pull:`1964`) :user:`marcelotduarte`
#)  tests: rewrite create_package to support dedent (:pull:`1960`) :user:`marcelotduarte`
#)  fix: bdist_rpm to pass tests in python 3.12b4 (:pull:`1963`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`1959`) :user:`pre-commit-ci`
#)  Bump version: 6.16.0-dev1 → 6.16.0-dev2 :user:`marcelotduarte`
#)  chore: enable Python 3.12 wheels and remove universal2 (:pull:`1958`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.13.1 to 2.14.0 (:pull:`1957`) :user:`dependabot`
#)  hooks: add boto3 (:pull:`1955`) :user:`marcelotduarte`
#)  hooks: move sklearn hook to a submodule (:pull:`1954`) :user:`marcelotduarte`
#)  hooks: fix the sentry_sdk hook (:pull:`1953`) :user:`marcelotduarte`
#)  hooks: improve hook for pillow [macos] (:pull:`1952`) :user:`marcelotduarte`
#)  fix: add rpath in macos executable [conda macos] (:pull:`1951`) :user:`marcelotduarte`
#)  samples: fix pydantic sample to work python < 3.10 (:pull:`1949`) :user:`marcelotduarte`
#)  chore: add more coverage reports [skip ci] (:pull:`1950`) :user:`marcelotduarte`
#)  fix: detection of dependent files and python shared library [conda linux/macos] (:pull:`1946`) :user:`marcelotduarte`
#)  fix: copy dependent files on "lib" directory [macOS] (:pull:`1942`) :user:`marcelotduarte`
#)  fix: support clang -fno-lto [conda macos] (:pull:`1948`) :user:`marcelotduarte`
#)  test: xfail some tests when rpmbuild is not present (:pull:`1947`) :user:`marcelotduarte`
#)  fix: bdist_rpm should generate only binaries [linux] (:pull:`1945`) :user:`marcelotduarte`
#)  [pre-commit.ci] pre-commit autoupdate (:pull:`1944`) :user:`pre-commit-ci`
#)  bases: update base executables and util module :user:`marcelotduarte`
#)  chore: more fine tuning pytest options [ci skip] (:pull:`1941`) :user:`marcelotduarte`
#)  tests: build executable to test in a subprocess (:pull:`1940`) :user:`marcelotduarte`
#)  chore: fine tuning pytest options (:pull:`1939`) :user:`marcelotduarte`
#)  chore: tweak to remove excess of pylint and noqa (:pull:`1938`) :user:`marcelotduarte`
#)  chore: add basic support for Python 3.12 (:pull:`1925`) :user:`marcelotduarte`
#)  parser: support for lief 0.14 ParserConfig (:pull:`1924`) :user:`marcelotduarte`
#)  chore: drop support for python 3.7 (:pull:`1935`) :user:`marcelotduarte`
#)  chore: to use pre-commit.ci add skip option (:pull:`1936`) :user:`marcelotduarte`
#)  Bump version: 6.16.0-dev0 → 6.16.0-dev1 (:pull:`1933`) :user:`marcelotduarte`
#)  chore: use pytest-xdist to speed up the tests (:pull:`1932`) :user:`marcelotduarte`
#)  fix: zip_include_packages/zip_exclude_packages regression (:pull:`1922`) :user:`marcelotduarte`
#)  build(deps-dev): bump ruff from 0.0.272 to 0.0.275 (:pull:`1930`) :user:`marcelotduarte`
#)  tests: add more test cases for ModuleFinder class (:pull:`1929`) :user:`marcelotduarte`
#)  tests: add more samples to tests (:pull:`1928`) :user:`marcelotduarte`
#)  chore: use pytest-datafiles to run tests in temporary path (:pull:`1927`) :user:`marcelotduarte`
#)  build(deps-dev): bump pytest from 7.3.2 to 7.4.0 (:pull:`1926`) :user:`dependabot`
#)  chore: cleanup tests and dependencies (:pull:`1923`) :user:`marcelotduarte`
#)  build(deps): update setuptools requirement from <68,>=62.6 to >=62.6,<69 (:pull:`1919`) :user:`dependabot`
#)  build(deps-dev): bump pytest-mock from 3.10.0 to 3.11.1 (:pull:`1918`) :user:`dependabot`
#)  chore: bump ruff 0.0.272 and fix local/system dependencies (:pull:`1914`) :user:`marcelotduarte`
#)  linux: bdist_rpm depends on rpmbuild being installed (:pull:`1913`) :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.13.0 to 2.13.1 (:pull:`1909`) :user:`dependabot`
#)  build(deps-dev): bump pytest from 7.3.1 to 7.3.2 (:pull:`1908`) :user:`dependabot`
#)  Bump version: 6.15.0 → 6.16.0-dev0 (:pull:`1905`) :user:`marcelotduarte`
#)  samples: add scipy sample (:pull:`1904`) :user:`marcelotduarte`
#)  hooks: fix scipy hooks used in zip_include_packages (:pull:`1903`) :user:`marcelotduarte`
#)  samples: update matplotlib sample using Wx (and remove deprecated test) (:pull:`1902`) :user:`marcelotduarte`
#)  samples: add a new matplotlib sample using Tk (:pull:`1901`) :user:`marcelotduarte`
#)  hooks: fix matplotlib hooks used in zip_include_packages (:pull:`1897`) :user:`marcelotduarte`
#)  hooks: improve scipy hooks (:pull:`1896`) :user:`marcelotduarte`
#)  fix: increase maximum recursion depth (:pull:`1890`) :user:`marcelotduarte`
#)  bases: update base executables and util module :user:`marcelotduarte`
#)  build(deps-dev): bump cibuildwheel from 2.12.3 to 2.13.0 (:pull:`1893`) :user:`dependabot`
#)  build(deps-dev): bump pytest-cov from 4.0.0 to 4.1.0 (:pull:`1891`) :user:`dependabot`
#)  Exit with non-zero exit code on exception (:pull:`1783`) :user:`johan.ronnkvist`
