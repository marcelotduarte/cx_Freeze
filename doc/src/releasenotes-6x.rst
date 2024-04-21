6.x releases
############

Version 6.15 (May 2023)
-----------------------

#)  Breaking changes:
	- chore: remove the latest camelCase in Executable api (:pull:`1809`)
	- chore: use utf-8 encoding with read_text (:pull:`1817`)
	- chore: map internal exception classes to setuptools (:pull:`1866`)

#)  New or improved hooks for:
	- hooks: split more hooks in a separate module (:pull:`1790`)
	- hooks: add suport for matplotlib 3.7 (:pull:`1791`)
	- hooks: improved hook for pytorch (:pull:`1804`)
	- fix: add tcl8 directory to bases and fix tkinter hooks (:pull:`1812`)
	- hooks: improved hook for matplotlib 3.7 work with bdist_msi (:pull:`1815`)
	- fix: matplotlib hooks (:pull:`1818`, :pull:`1819`)
	- hooks: pyside6/pyqt6 - fix svg and pdf, docs, modules (:pull:`1827`)
	- hooks: pyside6 - check for conda (:pull:`1828`)
	- hooks: include a qt.conf for pyqt6-webengine to work (:pull:`1829`)
	- hooks: include a qt.conf for pyside2-webengine to work (:pull:`1832`)
	- hooks: add new qt plugins based on the docs (:pull:`1835`)
	- hooks: add pyimagej and jpype (:pull:`1842`)
	- hooks: add librosa and lazy_loader hooks (:pull:`1856`)
	- hooks: numpy can be used in conda-forge without mkl [windows] (:pull:`1867`)
	- hooks: add pyreadstat (:pull:`1883`)

#)  Linux:
	- fix: use latest manylinux release to fix tkinter in Python 3.11 (:pull:`1830`)
	- fix: setuptools is unbundled on Gentoo (:pull:`1864`)

#)  Windows:
	- windows: fix file version with four elements (:pull:`1772`)
	- windows: fix error using CX_FREEZE_STAMP=pywin32 (:pull:`1773`)
	- windows: put all msvcr dlls in build_exe top directory (:pull:`1780`)
	- fix: copy all top dependencies [windows,conda] (:pull:`1799`)
	- fix: copy all top dependencies [mingw] (:pull:`1859`)

#)  Documentation:
	- docs: improve options documentation and fix typos (:pull:`1805`)

#)  Improvements/Refactor/Bugfix:
	- Revert "commands: accepts space-delimited string lists" (:pull:`1768`)
	- freezer: fix importerror when using 'path' option (:pull:`1785`)
	- Check that parent directory exists before writing to file (:pull:`1793`)
	- fix: parse namespace packages as packages in zip options (:pull:`1820`)
	- fix: restore build-exe option of build command (now deprecated) (:pull:`1823`)
	- Fix code for year 2038 (:pull:`1860`)
	- fix: ignore recursion into .git subdirectories (:pull:`1884`)

#)  Project:
	- Declare support for setuptools 67.x (:pull:`1782`)
	- Use CodeQL tools for scanning (:pull:`1766`)
	- Use bump2version tag_name (:pull:`1769`)
	- Upgrade pre-commit tools (:pull:`1774`)
	- freezer: pylint ready (:pull:`1781`)
	- dependabot: add package-ecosystem for pip (:pull:`1792`)
	- chore: use ruff (:pull:`1798`, :pull:`1800`, :pull:`1801`, :pull:`1802`, :pull:`1803`, :pull:`1836`)
	- chore: change Makefile to call pylint separated of others tools (:pull:`1807`)
	- chore: update python dependencies (:pull:`1808`, :pull:`1822`)
	- chore: add python version to dependabot (:pull:`1810`)
	- chore: use code_object_replace_function if possible (:pull:`1816`)
	- chore: normalize filename and use map (:pull:`1839`)
	- chore: Generate coverage report (:pull:`1843`)

Version 6.14 (January 2023)
---------------------------

#)  New or improved hooks for:
	- hooks: Add charset_normalizer (:pull:`1758`)
	- hooks: Add shapely (:pull:`1725`)
	- hooks: Add sklearn hook (:pull:`1715`)
	- hooks: Add pytorch (:pull:`1720`)
	- hooks: Update scipy hook (:pull:`1716`)
	- hooks: fix sqlite3 hook in python embed (:pull:`1707`)

#)  Linux:
	- Support to build musllinux wheels (:pull:`1687`)
	- project: Improve patchelf dependency specification (:pull:`1722`)

#)  Windows:
	- startup: Do not limit PATH (revert #1659 partially), limit dll search path (:pull:`1675`)
	- Ignore pylint error for deprecated module msilib (:pull:`1682`)
	- Update to cx_Logging 3.1 and remove hacks for previous version (:pull:`1688`)
	- [windows] Compile base executables with generic names depending on cache_tag (:pull:`1712`)
	- [windows] build-wheel: maintain base executables on git (:pull:`1713`)
	- [windows] build-wheel: fix git rm (use --ignore-unmatch instead) (:pull:`1714`)
	- [windows] build-wheel: fix git branch (:pull:`1717`)
	- [windows] setup: optional compilation in editable mode (:pull:`1718`)

#)  Documentation:
	- pin sphinx to 5.3.0 (:pull:`1691`)
	- docs: fix typo (:pull:`1697`)
	- doc: Add keywords for setup() and reorganize read order (:pull:`1728`)
	- Update copyright year (:pull:`1749`)
	- docs: use 'furo' theme for sphinx (:pull:`1750`)
	- doc: cleanup after use of furo theme (:pull:`1755`)
	- doc: improve documentation about setup script (:pull:`1756`)
	- project and doc: tweak formatting and ordering (:pull:`1762`)
	- Small fixes in code and documentation (:pull:`1738`)

#)  Improvements/Refactor/Bugfix:
	- Include copy of cx_Freeze license with frozen applications (:pull:`1672`)
	- license: move update_frozen_license to a pre-commit (:pull:`1676`)
	- Move OS constants to _compat module (:pull:`1709`)
	- install: run() method needs to exist (:pull:`1747`)
	- Fix the subclassing of internal commands (regression introduced in #1746) (:pull:`1759`)
	- commands: accepts space-delimited string lists (:pull:`1761`)

#)  Project:
	- Support Python 3.11 and set it as default in CI (:pull:`1681`)
	- Drop python 3.6 (:pull:`1670`)
	- Drop the external dependency on importlib-metadata (:pull:`1692`)
	- Drop the external dependency on packaging (:pull:`1730`)
	- Python type hints - upgrade syntax (:pull:`1703`)
	- Cleanup (:pull:`1760`)
	- setup: move metadata to pyproject.toml (setuptools 61+) (:pull:`1677`)
	- pre-commit: fix files that trigger the hook (:pull:`1690`)
	- Update pre-commit dependencies (:pull:`1693`)
	- update dev dependencies (:pull:`1701`)
	- project: add/fix urls (:pull:`1708`)
	- build-wheel: add missing sdist files (:pull:`1711`)
	- dist: Use another aproach to export DistributionMetadata (:pull:`1726`)
	- build: setuptools has 'build' command since v62.4.0 (:pull:`1729`)
	- dist: Use setuptools plugins to extend Distribution instead of subclassing (:pull:`1733`)
	- Use setuptools Distribution directly (:pull:`1736`)
	- Add build_exe as subcommand of setuptools build (plugin) (:pull:`1737`)
	- Add/update commands (provisional) and minor tweaks (:pull:`1746`)
	- Add dependabot (:pull:`1752`)
	- Declare support for setuptools 66.0 (:pull:`1753`)
	- Ignore build time error (:pull:`1754`)

#)  Samples:
	- samples: Add simple samples using pyproject.toml and setup.cfg (:pull:`1757`)

Version 6.13 (October 2022)
---------------------------

#)  New or improved hooks for:
	- hooks: Add hooks for PyQt6 (6.3.1 and 6.4.0) (:pull:`1664`)
	- hooks: support for new pyside6 6.4.0 (:pull:`1642`)
	- hooks: support for PySide6 6.4.0 on MSYS2 (:pull:`1655`)

#)  Windows:
	- Fix the filename of .msi file generated by bdist_msi. (:pull:`1591`)
	- Improvements related to bdist_msi --target_name (:pull:`1648`)
	- initscripts: Separate the code needed by windows and mingw and fix the path usage. (:pull:`1652`)
	- Fix missing dlls in build root directory [mingw] (:pull:`1653`)
	- Ensure python3.dll is loaded in some python versions (bpo-29778) (:pull:`1657`)
	- Fix dependency target to work better with MSYS2 (:pull:`1658`)
	- startup: limit the PATH in all windows environments (:pull:`1659`)
	- setup: Fix python compatibility, especially on Windows (:pull:`1656`)
	- parser: lief >= 0.12 is required [windows] (:pull:`1661`)

#)  Samples:
	- samples: fix demo scripts for pythonnet 3 (:pull:`1643`)
	- samples: Add samples for PyQt6 and add readme to some qt samples (:pull:`1663`)

#)  Improvements/Refactor/Bugfix:
	- Refactor ci/requirements.py (:pull:`1644`)
	- tests: add mores tests for bdist_msi (:pull:`1646`)
	- Do not translate newlines (generate identical file across OS) (:pull:`1645`)
	- Fix warning and test docs. (:pull:`1647`)
	- Monkey patch setuptools sandbox to get a better run_setup (:pull:`1649`)
	- tests: cleanup files and directories created (:pull:`1650`)
	- use os.fspath() instead of str() (:pull:`1660`)

Version 6.12 (October 2022)
---------------------------

#)  Linux:
	- Support Linux binary wheel for arm64 (:pull:`1539`)

#)  macOS:
	- darwintools: fix bug in the processing of certain dynamic library references (:pull:`1521`)
	- darwintools: Further clean-up of path resolver code. (:pull:`1529`)
	- Make various errors in darwintools show a warning, rather than terminating freeze (:pull:`1593`)

#)  Windows:
	- freezer: Fix dependency target to avoid duplicates [windows] (:pull:`1623`)
	- Call InitializePython from Service_Main instead of wmain. (:pull:`1572`)
	- bdist_msi: sort options (:pull:`1519`)
	- bdist_msi: Fix unnecessary 'running egg_info' (:pull:`1520`)
	- bdist_msi: Fix target-name and target-version (:pull:`1524`)

#)  New or improved hooks for:
	- Improve tkinter hook to work on all OS (:pull:`1526`)
	- hooks: add hook for orjson (:pull:`1606`)
	- hooks: Ensure include_files only if file exists. (:pull:`1627`)
	- hooks: Add hook for tokenizers (:pull:`1628`)
	- hooks: only bcrypt < 4.0 requires cffi (:pull:`1607`)
	- hooks: update cryptography hook (:pull:`1608`)
	- hooks: bcrypt and cryptography hooks must work with msys2 (:pull:`1609`)
	- qt hooks: Put pyqt5 and pyside2 hooks in separate modules (:pull:`1531`)
	- qt hooks: New pyside6 hooks (:pull:`1533`)
	- qt hooks: fix qthooks imports/exports and add an optional debug mode (:pull:`1551`)
	- qt hooks: Add PyQt5/Pyside2/PySide6 hooks for QtDesigner module (:pull:`1552`)
	- qt hooks: Rewrite pyqt hooks to query Qt Library paths instead of guessing (:pull:`1555`)
	- qt hooks: Restructures qt hooks into subpackages for easier troubleshooting. (:pull:`1561`)
	- qt hooks: set some default paths and fix copies (:pull:`1565`)
	- qt hooks: add resources to PySide2 hooks to work on more environments (:pull:`1566`)
	- qt hooks: extend copy_qt_files to fix pyqtweb (:pull:`1568`)
	- qt hooks: a fix for conda-forge linux (pyside2) (:pull:`1585`)
	- qt hooks: fix the location of auxiliary files of webengine (pyqt5) (:pull:`1586`)
	- Improve opencv-python hook (:pull:`1536`)
	- Improve opencv-python hook on macos (:pull:`1538`)
	- Improve opencv hook for conda linux (:pull:`1556`)
	- Support msys2 in opencv-python hooks and use optimized mode (:pull:`1601`)
	- Restore PyYaml hook (:pull:`1542`)
	- Support for pythonnet 3.0 (:pull:`1600`)
	- hooks: Refactor as a subpackage (:pull:`1528`)
	- hooks: Put numpy hook in separate module (:pull:`1532`)
	- hooks: split Crypto hook in a separate module (:pull:`1602`)
	- hooks: split scipy hook in a separate module (:pull:`1603`)

#)  Samples:
	- samples: Add orjson sample (:pull:`1605`)
	- samples: pyqt5, pyside2 and pyside6 in optimized mode (:pull:`1587`)
	- New pyqt5 simplebrowser sample (adapted from pyside2 sample) (:pull:`1567`)
	- Use pyside6 example simplebrowser as sample (:pull:`1543`)
	- New opencv-python sample (:pull:`1535`)
	- Use the same tkinter sample as used in python (:pull:`1525`)
	- samples: add PhotoImage to tkinter (:pull:`1581`)
	- samples: adapt qt samples to use get_qt_plugins_paths (:pull:`1636`)

#)  Improvements/Refactor/Bugfix:
	- fix setuptools 61+ package discovery and other fixes for 62+ (:pull:`1545`)
	- fix setup to work with setuptools 64.x and 65.x (:pull:`1588`)
	- importlib-metadata >= 4.12.0 raise ValueError instead of returning None (:pull:`1625`)
	- Fixed ValueError / importlib_metadata problem (:pull:`1630`)
	- Fix readthedocs for 6.11
	- pin sphinx 5.0.1 and fix the support for it (:pull:`1512`)
	- update issue template (:pull:`1515`)
	- update dev dependencies (:pull:`1516`)
	- module: Fix .dist-info with subdirectories (:pull:`1514`)
	- Add parse as pylint-ready module (:pull:`1527`)
	- Remove deprecated options in build_exe and bdist_mac (:pull:`1544`)
	- Requires permanent use of lief package on windows (:pull:`1547`)
	- Add a workaround to compile with --no-lto if LTO linking fails (:pull:`1549`)
	- Fix a warning compiling with gcc 12.1 (:pull:`1550`)
	- finder: extend _base_hooks to include hooks in directories (:pull:`1557`)
	- update dev dependencies (:pull:`1558`)
	- setup: use find_packages and include_package_data for simplicity (:pull:`1559`)
	- samples: move to root (:pull:`1560`)
	- finder: extend include_file_as_module to include submodule (:pull:`1562`)
	- bases and initscripts: lowercase to remove pylint invalid-name (:pull:`1563`)
	- Update dev dependencies (:pull:`1584`)
	- tweak the bdist_rpm test (:pull:`1596`)
	- Add test for cx_Freeze.command.bdist_msi (:pull:`1597`)
	- freezer: copy package data using _copy_files to correctly parse dependencies (:pull:`1610`)
	- Improve makefile (:pull:`1619`)
	- Update dev dependencies (:pull:`1620`)
	- Cleanup to support/test with python 3.11b3 (:pull:`1518`)
	- feezer: use internal _create_directory (create the parents, verbose) (:pull:`1635`)

#)  Documentation:
	- Fixed a broken link in documentation (:pull:`1618`)
	- Improved documentation of initial_target_dir option on bdist_msi. (:pull:`1614`)
	- Add FAQ item for big installations (:pull:`1583`)

Version 6.11 (June 2022)
---------------------------

#)  Main Improvements:
	- First step to support static libpython (:pull:`1414`)
	- Set the path to search for modules, and fix the path for built-in modules (:pull:`1419`)
	- New release process relies on bump2version (:pull:`1365`)
	- Improve code to cache dist-info files and convert egg-info to dist-info (:pull:`1367`)
	- Compile base executables with generic names depending on SOABI (:pull:`1393`)
	- Add CI with a pre-commit file (:pull:`1368`)
	- Introduce tests in the GitHub CI (:pull:`1381`)
	- Get rid of some calls to deprecated module distutils (:pull:`1445`)
	- Borrow bdist_rpm from python 3.10 (:pull:`1446`)
	- Borrow bdist_msi from python 3.8 (:pull:`1447`)
	- pin setuptools to a range that works (:pull:`1453`)

#)  Linux:
	- Support for using embedded manylinux static libraries (:pull:`1504`)
	- Fix symlinks to avoid duplicate the target (:pull:`1424`)
	- Fix incorrect default bin path includes (:pull:`1425`)

#)  macOS:
	- Support for using macos static libraries (:pull:`1505`)

#)  Windows:
	- Convert PEP440 version scheme to windows scheme (:pull:`1392`)
	- Lief 0.12 supports delay_imports (:pull:`1426`)
	- LIEF 0.12 supports Python 3.10 (:pull:`1433`)

#)  New or improved hooks for:
	- Added additional hooks for the Qt sqldrivers and styles plugins. (:pull:`1371`)
	- Fix hooks for PySide2 5.15.2.1 (:pull:`1396`)
	- Optimizing and adding some Qt hooks (:pull:`1398`)
	- Use pathlib in qt hooks to always use posix paths as qt does (:pull:`1399`)
	- Add hooks for Pyside2.QtWebEngine* (and pyqtwebengine) (:pull:`1479`)

#)  Samples:
	- Add PySide6 sample (:pull:`1442`)
	- Use pyside2 example simplebrowser as sample (:pull:`1478`)

#)  Improvements/Refactor/Bugfix:
	- Minor tweaks with black (:pull:`1364`)
	- Run isort over the code base (:pull:`1366`)
	- Fixes some errors found by pylint (:pull:`1369`)
	- Fix requirements (:pull:`1373`)
	- Build in isolated mode for python 3.6-3.9 (:pull:`1374`)
	- Fix pre-commit configuration (:pull:`1375`)
	- Skip isort in imports_sample test to fix errors (:pull:`1383`)
	- Update MANIFEST.in and Makefile (:pull:`1391`)
	- Fix the default module name in IncludeFile (:pull:`1400`)
	- pin sphinx to 4.4.0 and fix the support for it (:pull:`1401`)
	- Fix some requirements and versions (:pull:`1402`)
	- Use blacken-docs for python code blocks in the docs (:pull:`1403`)
	- Fix a test after #1402 (:pull:`1404`)
	- Use sphinx rdt theme and minor tweaks (:pull:`1405`)
	- Use new build option in rdt to use py39 (:pull:`1406`)
	- Add pre-commit-sphinx (:pull:`1407`)
	- Add pip-tools pre-commit and enable setup-cfg-fmt (:pull:`1411`)
	- Use Path in setup (:pull:`1412`)
	- Use a self made requirements sync instead of piptools (:pull:`1413`)
	- Add cached_property (and a compatible function) for planned use (:pull:`1417`)
	- readme: To install the latest development build (:pull:`1418`)
	- finder: refactor load_module (:pull:`1420`)
	- The built-in modules are determined based on the cx_Freeze build (:pull:`1421`)
	- Some changes to satisfy the linters (:pull:`1422`)
	- Enable flake8 in pre-commit (:pull:`1423`)
	- Enable flake8 in samples (:pull:`1427`)
	- Bump black from 22.1.0 to 22.3.0 (:pull:`1428`)
	- Enable flake8 in tests (:pull:`1429`)
	- Enable pylint (limited to tests) (:pull:`1430`)
	- Update python dependencies (:pull:`1432`)
	- freezer: refactor to 'consider using with' (:pull:`1434`)
	- finder: use pep8 names (and enable pylint for it) (:pull:`1435`)
	- hooks: fixes docstrings and other lint warnings (:pull:`1436`)
	- hooks: new utility function copy_qt_data (:pull:`1437`)
	- hooks: use function attribute to avoid a pylint warning (:pull:`1438`)
	- hooks and setup are ready to pylint (:pull:`1439`)
	- More configuration to pylint (:pull:`1440`)
	- Fix the main docstring for some modules (:pull:`1441`)
	- Two more modules are ready for pylint. (:pull:`1443`)
	- Add cli and dist as pylint-ready modules (:pull:`1444`)
	- bdist_rpm: Make code style suitable for use in cx_Freeze (:pull:`1448`)
	- bdist_rpm: merge the code to make a unique class (:pull:`1449`)
	- bdist_msi: convert to utf8, apply pyupgrade, black and isort (:pull:`1452`)
	- Declare the new subpackage cx_Freeze.command (:pull:`1451`)
	- bdist_msi: get rid of distutils (:pull:`1454`)
	- bdist_msi: Pass pylint and flake8 (:pull:`1455`)
	- initscripts: pylint ready (:pull:`1456`)
	- bdist_rpm: condicional import (:pull:`1457`)
	- bdist_msi: move all the code to the command subpackage (:pull:`1458`)
	- Document the new code layout (:pull:`1459`)
	- Fix pylint configuration (:pull:`1460`)
	- bdist_mac: move macdist to new name and fix lint errors (:pull:`1461`)
	- bdist_*: fix some pylint invalid-name (:pull:`1462`)
	- Tests: enable a test by platform (:pull:`1463`)
	- build,install: move these commands to the command subpackage (:pull:`1464`)
	- build_exe: move this command to the command subpackage (:pull:`1465`)
	- install_exe: move this command to the command subpackage (:pull:`1466`)
	- install: suppress known deprecation (:pull:`1467`)
	- build: merge the code from distutils to the Build class (:pull:`1468`)
	- The python used to compile and to build is always the same [conda] (:pull:`1469`)
	- build: minor tweaks (:pull:`1471`)
	- pre-commit autoupdate and minor tweaks with pylint (:pull:`1472`)
	- Move setup() and refactor to avoid a future circular import in Freezer (:pull:`1473`)
	- setup: more pylint (:pull:`1474`)
	- Using a trick to get around a dependency on distutils. (:pull:`1475`)
	- CI in one file and cache pip dependencies (:pull:`1476`)
	- tests: Add test for build command (:pull:`1477`)
	- build_exe: fix a bug in the build_exe option (:pull:`1480`)
	- bdist_msi: move user_options to main code, excluding unused options (:pull:`1481`)
	- tests: add find_spec test (and remove similar sample) (:pull:`1482`)
	- Extend setuptools.sandbox.run_setup to work with cx_Freeze setup(). (:pull:`1484`)
	- tests: support for tests using Path (:pull:`1485`)
	- tests: add plist_items test (and remove similar sample) (:pull:`1486`)
	- tests: remove a no longer suppported method (:pull:`1487`)
	- tests: add a test for bdist_rpm (:pull:`1488`)
	- pre-commit: fix pyupgrade configuration (:pull:`1489`)
	- doc: Enable text wrapping in table cells using rdt_theme (:pull:`1496`)
	- Update issue templates (:pull:`1507`)
	- update dev dependencies (:pull:`1508`)


Version 6.10 (January 2022)
---------------------------

#)  Improvements:
	- Implements Parser interface to create an abstraction to parse binary
	  files (:pull:`1313`)
	- Implements basic PEParser interface (:pull:`1314`)
	- Helper to create and return a Path-like temporary directory
	  (:pull:`1338`)
	- Use build and tweak requirements (:pull:`1343`)
	- Add a basic pyproject.toml for build and tools (:pull:`1355`)

#)  Refactor and bugfix for all systems:
	- importlib.metadata is no longer provisional in Python 3.10 (:pull:`1316`)
	- Add a new _compat module (:pull:`1317`)
	- Prioritize importlib_metadata in versions lower than 3.10 (:pull:`1353`)
	- Fix an overwrite of silent variable in parser (:pull:`1322`)
	- Copy top dependencies only once (:pull:`1336`, :issue:`1304`,
	  :issue:`1333`)
	- Change the place to set version and set new year (:pull:`1350`)
	- Add more files to the source distribution (:pull:`1349`)
	- Minor tweaks in setup.cfg and add a missing version.py (:pull:`1351`)
	- Avoid error when cx_Freeze.util is not build yet (:pull:`1352`)
	- Use helper TemporaryPath in module (:pull:`1354`)

#)  Linux:
	- Implements ELFParser interface merging patchelf (:pull:`1315`)
	- Use PyPI patchelf rather than installed by OS (:pull:`1341`)

#)  Windows:
	- Drop references to shlwapi.dll on Windows to improve performance
	  (:pull:`1318`)
	- Use the dlltool provided in the same directory as gendef (:pull:`1319`)
	- Update manifest.txt to match python.manifest (:pull:`1320`)
	- Search dlls in sys.path, then in the path [windows] (:pull:`1323`)
	- Use PySys_SetArgvEx in windows too. (:pull:`1324`)
	- Add lief as dependency for windows (:pull:`1325`)
	- Support Application Manifests in Windows (:pull:`1326`, :issue:`385`,
	  :issue:`997`, :issue:`1305`)
	- Creates a manifest for an application that will request elevation
	  (:pull:`1327`, :issue:`1188`)
	- Ignore when lief is not available/installed, like in MSYS2 (:pull:`1328`)
	- util: style changes (:pull:`1329`)
	- Support Path in BeginUpdateResource and fix UpdateResource (:pull:`1330`)
	- Move version stamp to winversioninfo module (:pull:`1331`)
	- Add a simple test to winversioninfo (:pull:`1332`)
	- Implement version stamp [windows][experimental] (:pull:`1334`)
	- Workaround a bug in lief with utf-8 filenames [windows] (:pull:`1339`)
	- Use lief to detect dependencies [windows][experimental] (:pull:`1344`,
	  :issue:`665`)

#)  Samples:
	- Extend the 'icon' sample to use an admin manifest (:pull:`1340`)

#)  Documentation:
	- Documentation for manifest and uac-admin options (:pull:`1337`)
	- Update docs for patchelf (:pull:`1342`)


Version 6.9 (December 2021)
---------------------------

#)  Improvements:
	- Extend Module.in_file_system to support an optimized mode (:pull:`1301`)

#)  Refactor and bugfix for all systems:
	- Fix Implicit Namespace Packages (:pull:`1290`, :issue:`1276`)
	- Extend the support for vendored subpackages (:pull:`1294`)
	- Common: Prevent memory leaks on fail (:pull:`1245`)
	- Merge dis._unpack_opargs into scan_code to be able to fix a bug in py310
	  (:pull:`1306`)
	- Fix some print and f-string (:pull:`1246`)
	- fixing enumerations (:pull:`1263`)
	- Fixes for the existing nose tests (:pull:`1234`)
	- Generate `dev-requirements.txt` + improve readme for contributors wanting
	  to run tests (:pull:`1224`)
	- Convert existing tests to pytest + increase coverage (:pull:`1255`)

#)  Linux:
	- Fix relative path in dependencies, detected in miniconda linux
	  (:pull:`1258`)
	- Create symlinks in the target (:pull:`1292`, :issue:`750`)

#)  macOS:
	- fix bugs in certain subprocess calls (:pull:`1260`)
	- Apply ad-hoc signature to modified libraries (:pull:`1251`)

#)  Windows:
	- Set REINSTALLMODE to force installing same-version executables
	  (:pull:`1252`, :issue:`1250`)

#)  New or improved hooks for:
	- ctypes/libffi (:pull:`1279`)
	- flask-compress (:pull:`1295`, :issue:`1273`)
	- opencv-python (:pull:`1278`, :issue:`1275`)
	- PyQt5 hooks (:pull:`1302`, :issue:`1261`)
	- PySide2 - Linux only (:pull:`1302`)
	- sentry-sdk modules (:pull:`1282`)

#)  Samples:
	- Update PyQt5 sample (:pull:`1307`)

#)  Documentation:
	- Update the FAQ (:pull:`1247`)
	- Update msi doc (:pull:`1248`)
	- fade to black (:pull:`1291`)
	- docs: new item in faq (:pull:`1298`)
	- docs: open external links in a tab (:pull:`1299`)
	- prepare to release with python 3.10 support (:pull:`1308`)


Version 6.8 (September 2021)
----------------------------

#)  Improvements:
	- Support pathlib in ModuleFinder (:pull:`1153`)
	- Use Path in Module.file (:pull:`1158`)
	- Use Path in _replace_paths_in_code (:pull:`1159`)
	- Use Path in Module.path (:pull:`1160`)
	- Convert code in hooks to use Path (:pull:`1161`)
	- Use path.iterdir to simplify a code block (:pull:`1162`)
	- Use Path in executable module (:pull:`1163`)
	- Use Path in ModuleFinder.zip_includes (:pull:`1164`)
	- Use Path in process_path_specs (:pull:`1167`)
	- Use Path in Freezer include_files and zip_includes (:pull:`1168`)
	- Use Path in Freezer.targetdir and some related code (:pull:`1169`)
	- Use Path in Freezer._copy_file and almost remaining related code
	  (:pull:`1172`)
	- Use Path in Executable icon and shortcut_dir (:pull:`1173`)
	- Use Set[Path] in dependent_files (:pull:`1215`)
	- Use subprocess (:pull:`1214`)
	- Add more options to cxfreeze script and tweak the docs (:pull:`1174`)

#)  Refactor and bugfix for all systems:
	- Remove unused and unnecessary code (:pull:`1142`)
	- Add some old modules to exclude list (:pull:`1149`)
	- Fix a last minute change and tweak docstrings (:pull:`1154`)
	- Include files (from a directory) is ignoring the exclude dependencies
	  option (:pull:`1216`)
	- Add more typing to freeze (:pull:`1218`)
	- Create permanent cx_Freeze/bases (:pull:`1227`)
	- Make Freezer.targetdir a property to improve a bit (:pull:`1170`)
	- Code analysis, pep8, f-string (:pull:`1177`)
	- Complementary fixes (:pull:`1179`)
	- Use setuptools instead distutils a bit more (:pull:`1195`)

#)  Linux:
	- Fix py39 in ArchLinux using lto (in a different way than mac)
	  (:pull:`1146`, :issue:`1132`)
	- Patchelf calls supports Path type (:pull:`1178`)
	- Use Path (relative_to and parts) to rewrite the fix rpaths (:pull:`1181`)
	- Complementary patch to #1181 (:pull:`1201`)
	- Fix for Miniconda python in linux (:pull:`1219`)
	- Implement Patchelf.get_needed (still based on ldd) (:pull:`1220`)
	- Implement Patchelf.is_elf to optimize get_needed (:pull:`1221`)
	- Fix dependency target and rpath settings (:pull:`1223`)
	- Patchelf needs permission to write
	  (:pull:`1232`, :issue:`1171`, :issue:`1197`)
	- Disable strip with build --debug [linux] (:pull:`1235`, :issue:`1194`)

#)  macOS:
	- Use Path in darwintools and some pep8 (:pull:`1222`)
	- Fix MachORef in macdist and add-on tweaks to #1222 (:pull:`1229`)

#)  Windows:
	- Fix compatibility with msys2 python 3.9.6 (:pull:`1182`)
	- LLVM dlltool only supports generating an import library (:pull:`1187`)
	- Normalize paths at startup for MSYS2 python (:pull:`1193`)
	- Disable delay load to avoid 'Segmentation fault' in mingw 32 bits
	  (:pull:`1217`)
	- Support Path as parameter for some functions in C (:pull:`1225`)
	- Add a stub interface for util module (:pull:`1226`)
	- Recursing into directories to search for load order files (:pull:`1200`)
	- Fix program files folder for msi using mingw and some tweaks
	  (:pull:`1236`)

#)  New or improved hooks for:
	- _cffi_backend (cffi) (:pull:`1150`)
	- googleapiclient (:pull:`1151`, :issue:`1147`)
	- PyQt5 hooks (:pull:`1148`, :pull:`1155`, :pull:`1156`, :issue:`631`,
	  :issue:`846`, :issue:`972`, :issue:`1119`)
	- PySide2 (:pull:`1183`)
	- tzdata, zoneinfo and backports.zoneinfo
	  (:pull:`1198`, :pull:`1204`, :pull:`1208`)
	- pyzmq (:pull:`1199`)
	- numpy+mkl in conda (:pull:`1205`)

#)  Samples:
	- Fix code of some samples (:pull:`1145`)
	- Remove outdated sample (:pull:`1157`)
	- Improve sample to support pyzmq < 20 and timeout (:pull:`1190`)
	- Tweak pyqt5 and pyside2 samples (:pull:`1180`)
	- Improve PyQt5 and PySide2 samples (:pull:`1192`)

#)  Documentation:
	- Make distutils help and documentation more in line with cxfreeze script
	  (:pull:`1175`)
	- Update distutils build_exe help in docs (:pull:`1176`)
	- Remove distutils references in main docs (:pull:`1196`)
	- Better explain the miniconda installation (:pull:`1209`)
	- Minor updates to docs (:pull:`1230`)


Version 6.7 (July 2021)
-----------------------

#)  Improvements, refactor and bugfix for all systems:
	- Implemented multi levels for build_exe silent option (:pull:`883`)
	- Corrected silent_level to default to 0 (to agree with documentation) (:pull:`1046`)
	- Split up Freezer object (:pull:`1035`)
	- Ignores nonexistent files in dist-info (:pull:`1038`, :issue:`1034`)
	- Use setuptools build_ext to compile base executables and with names that dependes on python version and platform (:pull:`1054`)
	- Use sysconfig and others instead of some distutils modules (:pull:`1055`)
	- Handle the pre-copy task with the _pre_copy_hook method in the freezer (:pull:`1069`)
	- New method to handle platform dependent resources in the freezer (:pull:`1070`)
	- Minor tweaks to tidy up the code (:pull:`1079`)
	- Use wchar if possible. (:pull:`1080`)
	- Create cx_Freeze/bases if it doesn't exist (:pull:`1082`)
	- Use option blocks in the docs and add command line help from commands (:pull:`1097`)
	- Use a valid example in docs (:pull:`1098`)
	- Cleanup versionchanged; limit to 6.0+ (:pull:`1099`)
	- Improve the text of build_exe bin_* (:pull:`1100`)
	- Use of some Sphinx features to organize a bit (:pull:`1102`, :pull:`1138`, :pull:`1139`)
	- Implement Freeze._default_bin_path_includes for all platforms (:pull:`1108`)
	- Move some code to startup to unify the use of environ (:pull:`1112`)
	- Small changes to resolve code warnings (:pull:`1122`)
	- New method Module.update_distribution to update the cached distribution for the frozen executable (:pull:`1123`)
	- Implement DistributionCache.from_name (:pull:`1135`)
	- Use of black and pyupgrade (:pull:`1056`, :pull:`1085`, :pull:`1086`, :pull:`1086`, :pull:`1057`)
	- Use pep8 names in private functions in freezer (:pull:`1068`)
#)  Linux:
	- Fix the support for unix-like systems (:pull:`1067`, :issue:`1061`)
	- check in advance whether the dependency should be copied to avoid changing the rpath unnecessarily. (:pull:`1091`, :issue:`1048`)
	- Fix issue with strip in bdist_rpm (:pull:`1092`, :issue:`1048`)
	- Improve installation docs for linux (:pull:`1095`)
	- Fix a buffer overflow introduced in :pull:`872` (:pull:`1047`)
	- Fix another flaw introduced in :pull:`872` (:pull:`1111`)
	- Fix regression introduced in :pull:`995` (and (:pull:`985`)) (:pull:`1090`, :issue:`1029`)
#)  macOS:
	- Added CFBundlePackageType and NSHighResolutionCapable by default to Info.plist of Darwin bundles (:pull:`1031`, :issue:`239`)
#)  Windows:
	- Transform filename to msilib.Binary for binary data (:pull:`1024`, :issue:`1019`)
	- Add extension registration on Windows (:pull:`1032`)
	- Support for icons with non-ascii names (:pull:`1066`)
	- New C function to update the PE checksum (or fix it in case it is zero) (:pull:`1071`, :issue:`315`, :issue:`1059`)
	- Use setuptools command to install a include file (:pull:`1072`)
	- Fix the support for non-ascii names in windows (:pull:`1077`, :issue:`835`)
	- PyEval_InitThreads is unecessary in py37+ and is deprecated in py39 (:pull:`1081`)
	- Set working directory in the Desktop shortcut (:pull:`1083`, :issue:`48`, :issue:`623`)
	- Improve documentation about bdist_msi (:pull:`1084`, :issue:`48`)
#)  New or improved hooks for:
	- pydantic (:pull:`1074`, :issue:`1052`)
	- scikit-image (skimage) (:pull:`1104`, :issue:`1101`)
	- plotly (:pull:`1105`, :issue:`1101`)
	- scipy (versions 1.6.3 to 1.7.0) (:pull:`1106`, :pull:`1134`, :issue:`1101`, :issue:`1129`)
	- numpy and numpy+mkl (versions 1.19.5 to 1.21.0) (:pull:`1113`, :pull:`1125`, :issue:`739`, :issue:`1110`)
	- six (:pull:`1115`)
	- hdfdict, h5py_wrapper and pytest-runner (:pull:`1116`, :pull:`1124`, :issue:`1118`)
#)  Samples:
	- pydantic (:pull:`1074`)
	- pythonnet-demo (python.NET sample based on it's demo) (:pull:`1088`, :issue:`1049`)

Version 6.6 (April 2021)
------------------------

#)  Improvements:
	- Enable python -m cx_Freeze syntax (:pull:`899`)
	- Standardize InitializePython on all platforms. (:pull:`872`)
	- Store a copy of cached dist-info (:pull:`958`)
	- Suppress additional output if --silent has been set. (:pull:`830`)
	- Only copy a file if should copy a file (:pull:`995`, :issue:`256`)
	- Refactor cache dist-info files to be extended (:pull:`957`)
	- Remove subfolders belonging to excluded modules (:pull:`922`)
#)  Linux:
	- Implements a new Patchelf interface for patching ELF files (:pull:`966`)
	- Improve the resolution of dependencies [Linux] (:pull:`967`)
	- Use -rpath explicitly (:pull:`940`)
#)  macOS:
	- Another way to detected the use of LTO (:pull:`895`)
	- Failed to create DMG file (applications_shortcut=True`) (:pull:`927`, :issue:`925`)
	- Fix plistlib.load call in macdist [py39] (:pull:`926`, :issue:`924`)
	- Improvements to dependency resolution on Darwin (:pull:`887`)
	- Tweak to only print warning if attempting to copy two mach-o files to the same location.  Only the first file used. (:pull:`915`, :issue:`913`)
#)  Windows:
	- Avoid duplicates of libpythonXX.so and pythonXX.ddl (:pull:`978`)
	- Rebirth of --include-msvcr - real support for vcruntime dlls [windows] (:pull:`973`, :issue:`367`)
	- Set lib directory as default for dll search [windows] (:pull:`1000`)
	- Speedup compiling on windows (:pull:`993`)
	- Support for delay load [mingw] (:pull:`1002`)
	- Support for delay load [windows] (:pull:`1001`)
	- Update to cx_Logging 3.0 (:pull:`909`, :pull:`994`, :pull:`996`, :pull:`998`, :pull:`1012`)
	- Use the delay load to compile Win32Service (:pull:`1003`)
#)  New or improved hooks for:
	- llvmlite (:pull:`1016`)
	- matplotlib (:pull:`971`)
	- mkl-service (:pull:`975`)
	- numpy (:pull:`970`, :pull:`968`)
	- pandas (:pull:`969`)
	- pycountry (:pull:`956`)
	- pyodbc (:pull:`1018`)
	- pyqtgraph (:pull:`1015`)
	- pyzmq 22 (:pull:`953`)
#)  Samples:
	- Add sample for pycountry (:pull:`955`)
	- Add sample for pyzmq (:pull:`954`)
	- Update the service sample and build (:pull:`886`)
	- Update PySide2 sample (:pull:`1011`)
	- Tweak samples (:pull:`888`)
#)  Bugfixes:
	- Force encoding of generated files to utf-8 (:pull:`1005`, :issue:`989`)
	- cx_Logging as submodule (:pull:`874`, :issue:`866`)
	- Avoid the __main__ module from pip wheel (:pull:`894`, :issue:`891`)
	- Fix regression introduced in PR #857 (:pull:`878`, :issue:`875`)
	- Fix typo (:pull:`877`, :issue:`866`)
	- Fix the pillow sample (:pull:`876`)
	- Fix the docs (:pull:`870`)
	- Fix regression introduced in #978 (:pull:`1010`)
	- Standardizes the target directory Freezer (and cxfreeze`) (:pull:`999`)
	- Fix regression introduced in PR #973 (:pull:`976`)
	- Fix PATH for anaconda/miniconda (:pull:`974`)
	- Starts freezing in a clean directory (:pull:`965`)
	- Fix a regression introduced in #798 (:pull:`945`, :issue:`932`)
	- fix regressions introduced in #843 (:pull:`920`, :issue:`919`)
	- Some packages use a directory with vendored modules (:pull:`906`, :issue:`900`)
	- IncludeModule has priority over ExcludeModule (:pull:`904`)
	- Better error checks (:pull:`902`)
	- Support for executable names that may not be valid identifiers (:pull:`889`, :issue:`884`)
	- Accept file without extension as source file to be backwards compatible (:pull:`893`)
#)  Refactor:
	- Update readme (:pull:`1022`)
	- Update installation docs (:pull:`1021`)
	- Modify cxfreeze script a bit (:pull:`1009`)
	- Reestructure ConstantModule (:pull:`1004`)
	- Invert the assignment to create a new list (:pull:`987`)
	- Refactor Freezer init (:pull:`985`)
	- New module exception (:pull:`984`)
	- Separates the freezer module classes (:pull:`983`)
	- Update code style in Modules (:pull:`982`)
	- build docs in build dir at project's root (:pull:`981`)
	- Minor update to code style (:pull:`980`)
	- update faq a bit (:pull:`977`)
	- Cleanup freezer copy file method (:pull:`964`)
	- Typo (:pull:`962`)
	- Change detection order and tweak formatting (:pull:`961`)
	- Refactor Module class attributes (:pull:`960`)
	- Fade to black (:pull:`946`, :pull:`1020`)
	- Distribute samples only with source code (:pull:`941`)
	- Add badges (:pull:`944`)
	- Revise docs a bit  (:pull:`943`)
	- Update in the docs the use of main branch (:pull:`942`)
	- remove unused files (:pull:`910`)
	- Update build-wheel (:pull:`903`)
	- Revert previous commit and fix the ident only (:pull:`882`)
	- Fix potential errors (:pull:`881`)
	- Code analysis (:pull:`880`)

Version 6.5 (January 2021)
---------------------------

#)  Improvements:
	- Refactor ModuleFinder to use importlib.machinery (:pull:`811`)
	- Executable target_name now has support for names with version (:pull:`857`)
	- The name of the target executable can be modified after the build
	  (:pull:`858`, :issue:`703`)
	- Use codeType.replace when in py38+ (optimized) (:pull:`836`)
	- Use a configuration file for Read the Docs (:pull:`818`)
	- Modernize code (Type annotation, PEP8, black, refactor)
	  (:pull:`815`, :pull:`832`, :pull:`837`, :pull:`838`, :pull:`839`,
	  :pull:`840`, :pull:`841`, :pull:`842`, :pull:`843`, :pull:`859`,
	  :pull:`860`, :pull:`861`, :pull:`864`, :pull:`865`, :pull:`868`)
#)  Windows:
	- Check if icon is valid
	  (:issue:`856`, :pull:`851`, :issue:`824`, :issue:`379`)
	- Warning about python from Windows Store (:pull:`867`, :issue:`856`)
#)  macOS:
	- Implemented a "plist_items" option on bdist_mac command (:pull:`827`)
	- Remove deprecated methods in macdist (:pull:`810`)
	- Fix a regression for macOS (:pull:`816`, :issue:`809`)
	- Fix a bug using macOS on Github Actions (:pull:`812`)
	- Marked rpath-lib-folder option as depreciated. (:pull:`834`)
#)  New or improved hooks for:
	- cryptography (:pull:`817`, :issue:`814`)
	- google.cloud.storage (:pull:`821`)
	- matplotlib (:pull:`807`, :issue:`805`)
	- pygments (:pull:`863`, :issue:`862`)
	- zoneinfo/tzdata (and backports.zoneinfo) (:pull:`854`)
#)  Samples:
	- Better pytz sample (:pull:`852`)
	- Sample for new library zoneinfo (py39) (:pull:`853`)
	- Sample to demonstrate the use a valid and an invalid icon (:pull:`850`)
#)  Bugfixes:
	- cx_Freeze.__version__ should be the package version
	  (:pull:`806`, :issue:`804`)
	- pin importlib_metadata to >=3.1.1 (:pull:`819`, :pull:`820`, :pull:`822`)
	- Correct test failures when initializing ModuleFinder (:pull:`833`)


Version 6.4 (November 2020)
---------------------------

#)  Improvements:
	- Improved the resolution of dependencies in darwin MachO files (:pull:`590`)
	- Documentation (:pull:`783`, :pull:`796`)
	- Release using GitHub Actions CI/CD workflows (:pull:`797`)
	- Apply pyupgrade (:pull:`801`)
	- Modernize code (Type annotation, PEP8, black, refactor, cleanup)
	  (:pull:`785`, :pull:`776`, :pull:`314`, :pull:`787`, :pull:`784`,
	  :pull:`786`, :pull:`788`, :pull:`789`, :pull:`793`, :pull:`794`,
	  :pull:`780`, :pull:`795`, :pull:`799`, :pull:`800`, :pull:`790`,
	  :pull:`798`)
#)  New or improved hooks for:
	- PyQt5 (:pull:`718`, :pull:`791`)
#)  Samples:
	- Added a sample to illustrate problem with importlib.util.find_spec
	  (:pull:`735`)
	- Sample for bdist_msi, summary_data option (:pull:`775`)
	- README for some samples; remove requirements.txt to avoid to be
	  interpreted by some sites as the requirements of cx_Freeze (:pull:`802`)
#)  Bugfixes:
	- Cause MSI file to be released at the end of bdist_msi command (:pull:`781`)


Version 6.3 (October 2020)
--------------------------

#)  Improvements:
	- Improve metadata using importlib.metadata (:pull:`697`)
	- New options in ``cxfreeze`` script; documentation updated (:pull:`742`)
	- The command line parser was rewritten and modernised using argparse
	  (:pull:`741`)
	- Documentation (:pull:`740`, :pull:`722`, :pull:`720`)
	- Cleanups (:pull:`766`, :pull:`746`, :pull:`744`, :pull:`743`,
	  :pull:`736`, :pull:`726`, :pull:`724`, :pull:`721`, :pull:`712`)
#)  New or improved hooks for:
	- google.cloud.storage (:pull:`708`)
	- google.crc32c (:pull:`737`)
	- matplotlib and numpy (:pull:`695`, :issue:`692`)
	- scipy (:pull:`725`)
	- sysconfig (:pull:`727`, :pull:`715`)
	- tensorflow (:pull:`710`)
#)  Linux:
	- Improve copy dependent files relative to source module file (:pull:`704`)
#)  Windows:
	- Check if upgrade-code is valid and document the valid format
	  (:pull:`711`, :issue:`585`)
	- Improve Windows GUID documentation (:pull:`749`)
	- Added option to bdist_msi to specify information for msi summary
	  information stream (:pull:`760`)
#)  macOS:
	- Fix the syspath for some version of python on macOS
	  (:pull:`719`, :issue:`667`)
#)  Samples:
	- Add pyside2 sample (:pull:`664`)
	- A sample for testing PyQt5 included in zip package (:pull:`717`)
	- Add pandas sample (:pull:`709`)
	- Added sample code to show the use of ConstantsModule / BUILD_CONSTANTS
	  (:pull:`729`)
#)  Bugfixes:
	- Ensure the copy of default python libraries in all platforms
	  (:pull:`706`, :issue:`701`)
	- Remove warning 'Distutils was imported before Setuptools'
	  (:pull:`694`, :issue:`693`)
	- Fix the use of compress and desambiguate the use of stat (:pull:`738`)
	- Small fix to handle a build constant that includes a "=" symbol
	  (:pull:`728`)
	- Fix issue when module.file is None (:pull:`707`)
	- Fix detect namespaces in py35 (:pull:`700`)
	- Set python initialization flags prior to Py_SetPath call to avoid
	  warnings (:pull:`751`)


Version 6.2 (July 2020)
-----------------------

#)  New or improved hooks for:
	- aiofiles (:pull:`600`)
	- babel (:pull:`577`)
	- bcrypt (:pull:`583`, :issue:`581`)
	- certifi (:pull:`690`)
	- cffi.cparser (:pull:`603`)
	- ctypes (for MSYS2 mingw) (:pull:`565`)
	- matplotlib (:pull:`574`, :issue:`569`)
	- pikepdf (:pull:`604`)
	- lxml (:pull:`604`)
	- pycryptodome (:pull:`602`)
	- pygments (:pull:`604`)
	- pkg_resources (:pull:`584`, :issue:`579`)
	- pytest (:pull:`617`)
	- setuptools (:pull:`608`)
	- uvloop (:pull:`689`)
#)  Linux:
	- Pass command line arguments in current locale (:pull:`645`, :issue:`611`)
#)  Windows:
	- Fixed multiprocessing pickling errors (:pull:`622`, :issue:`539`, :issue:`402`, :issue:`403`, :issue:`231`, :issue:`536`)
	- Ensure the copy of default python libraries (:pull:`640`)
	- Replace deprecated functions that will be removed in py4 - win32gui (:pull:`649`)
	- Exclude Tkinter from loaded modules (:pull:`576`, :issue:`567`)
	- Fixed "no module named 'scipy.spatial.cKDTree'" (:pull:`626`, :issue:`233`)
	- Fixed "no module named 'multiprocessing.pool'" (:pull:`627`, :issue:`353`)
	- Download cx_Logging to build Win32Service.exe when building from sources (:pull:`650`, :issue:`519`)
#)  macOS:
	- Fixing modification of PATH for single user install (:pull:`614`, :issue:`613`)
	- Make needed dirs when using include_resources (:pull:`633`)
	- Check for Mach-O using byte strings to allow case of non unicode chars (:pull:`635`)
	- Copy references from /usr/local (:pull:`648`)
#)  Documentation
	- Update doc and faq (:pull:`564`, :pull:`663`, :pull:`688`)
	- Initial work to be pep8 compliant (:pull:`572`, :pull:`582`)
#)  Misc
	- Fixed bug in ``cxfreeze`` script introduced in 6.1 (:issue:`560`).
	- Remove old packages/modules names, do not report as missing (:pull:`605`)
	- Better support for MSYS2 and Anaconda3 (:pull:`642`)
	- Support python 3.5.2 and up (:pull:`606`)
	- Support metadata to use by pkg_resources (:pull:`608`)
	- New commom function rebuild_code_object to be reusable (:pull:`629`)
	- Fix optimize option in python 3.8 (:pull:`641`)
	- Add --include-files option to ``cxfreeze`` script (:pull:`647`)
	- Replace the value of __package__ directly in the code (:pull:`651`)
	- Eliminate exclusion of ``dbm`` module since it is in Python 3 (:pull:`662`, :issue:`660`)
	- Detect namespace packages (:pull:`669`, :pull:`668`)
	- Installing from source requires setuptools (:pull:`687`)
	- Remove PyUnicode_FromUnicode (:pull:`673`)

Version 6.1 (January 2020)
--------------------------

#)  Added support for Python 3.8 (:pull:`545`, :pull:`556`).
#)  Added support for ``python setup.py develop`` (:pull:`502`).
#)  Use ``console_scripts`` in ``entry_points`` so that the commands
    ``cxfreeze`` and ``cxfreeze-quickstart`` run on Windows without the need
    for running a postinstall script (:pull:`511`).
#)  Added support for switching from per-user to per-machine installations on
    Windows (:pull:`507`).
#)  Fix installation if ``AlwaysInstallElevated`` policy is set on Windows
    (:pull:`533`).
#)  Updated default dependencies for Python 3 on Windows (:pull:`505`).
#)  Removed unused code (:pull:`549`).
#)  The default dependencies are now always copied into the lib folder instead
    of into the directory where the executable resides on Linux
    (:pull:`518`).
#)  Dependent files are now copied to the same relative directory as their
    location in the source on Linux (:pull:`494`).
#)  Added tests for commonly used packages like ``cryptography``, ``pillow``,
    ``sqlite``, ``pytz``, ``ctypes`` and ``distutils``
    (:pull:`508`, :pull:`537`, :pull:`546`, :pull:`555`, :pull:`557`).
#)  Fix regression with DLL dependencies introduced in 6.0 by :pull:`492`
    due to case differences (:pull:`512`).
#)  Fix regression with dependent files introduced in 6.0 by :pull:`297`
    for platforms other than macOS (:pull:`516`).
#)  The version of cx_Freeze is now defined in one place (:pull:`552`).
#)  Eliminate exclusion of ``gestalt`` module on platforms other than macOS
    since it exists outside of macOS.
#)  Improved hooks for ``sqlite3`` (:pull:`509`), ``cryptography``, and
    ``tkinter`` (:pull:`559`).
#)  Added hook for ``pytz`` (:pull:`554`).
#)  Improved hook infrastructure, permitting hooks to add constants that can
    be examined at runtime, determine whether a module is going to be stored in
    the file system and include files in the zip file.
#)  Improved documentation (:pull:`510`).


Version 6.0 (August 2019)
-------------------------

#)  Corrected support for Python 3.7 (:pull:`395`).
#)  Use importlib and other Python 3 improvements
    (:pull:`484`, :pull:`485`, :pull:`486`, :pull:`490`).
#)  Fixed issue with @rpath causing file copy errors on macOS (:pull:`307`).
#)  Replaced file() with open() and use context manager to ensure the file
    handle is closed and deleted (:pull:`348`).
#)  Corrected invalid version handling in bdist_msi (:pull:`349`, :issue:`340`).
#)  Corrected hook for clr module (:pull:`397`, :pull:`444`).
#)  Corrected documentation for compress option (:pull:`358`).
#)  Ensure that the pythoncom and pywintypes DLLs are found in the lib
    directory and not in the base directory (:issue:`332`).
#)  Always copy dependent files to root directory on macOS (:pull:`365`).
#)  Skip self referencing archive on macOS (:pull:`364`, :issue:`304`).
#)  Include doc directory in source distribution (:pull:`394`, :issue:`376`).
#)  Force msilib module to be reloaded in order to allow for the generation of
    multiple MSI packages in a single session (:pull:`419`).
#)  Added hook for PyQt5.QtPrintSupport module (:pull:`401`).
#)  Added ability to include an icon on the add/remove program window that pops
    up during installation (:pull:`387`).
#)  Prevent spurious errors from being printed during building on macOS by
    checking to see that a file is a Mach-O binary before adding it to the list
    of files it is checking the reference of (:pull:`342`, :issue:`268`).
#)  Avoid otool bug on macOS Yosemite (:pull:`297`, :issue:`292`).
#)  Added ability to specify environment variables that should be created when
    an MSI package is installed (:pull:`266`).
#)  Added support for including resources in an app bundle for macOS
    (:pull:`423`).
#)  Added absolute reference path option for macOS packages (:pull:`424`).
#)  Added CFBundle identifier for macOS packages (:pull:`427`, :issue:`426`).
#)  Added hook for copying SSL DLLs for Python 3.7+ on Windows (:pull:`470`).
#)  Added -municode flag when building on Windows with mingw32 (:pull:`468`).
#)  Added hook for pycparser (:pull:`446`).
#)  Fixed hook for zmq so it doesn't fail when there is no bundled libzmq
    library in the installed pyzmq package (:pull:`442`).
#)  Print error when fetching dependent files fails (:pull:`435`).
#)  Make executable writable before adding the icon
    (:pull:`430`, :issue:`368`).
#)  Dropped support for RPM and MSI packages for cx_Freeze itself since these
    are no longer supported by PyPI.
#)  Fix building console app with mingw32 (:pull:`475`).
#)  Force inclusion of the unicodedata module which is used by the socket
    module, and possibly others (:pull:`476`).
#)  Added hook for asyncio package (:pull:`477`).
#)  Added hook for idna package (:pull:`478`).
#)  Added hook for pkg_resources package (:pull:`481`).
#)  Added hook for gevent (:pull:`495`).
#)  Force .exe extension to be included on Windows, so that the same setup code
    can be used on both Linux and Windows (:pull:`489`).
#)  Added hook for Pillow (:pull:`491`).
#)  Improved hook for tkinter (:pull:`493`).
#)  Avoid attempting to check for dependent files on Windows when the file is
    not an executable or DLL (:pull:`492`).
#)  Ensure that only executable files are checked for dependencies in order to
    avoid spurious errors when checking for dependent files.
#)  Improved hook for matplotlib.


Version 6.0b1 (November 2017)
-----------------------------

#)  Dropped support for Python 2.x. Use cx_Freeze 5 for Python 2.x support.
#)  Instead of depending on the built-in functionality of searching for a zip
    file that looks like pythonxx.zip (which is disabled on some platforms like
    Ubuntu), set the Python path to include a subdirectory called "lib" and a
    zip file "lib/library.zip" on all platforms.
#)  Do not create version resource when version is omitted (:pull:`279`).
#)  Ensure the sqlite3 DLL is loaded in the same directory as the module which
    depends on it (:issue:`296`).
