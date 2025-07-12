6.x releases
############

Version 6.15 (May 2023)
-----------------------

#)  Breaking changes:
	- chore: remove the latest camelCase in Executable api (:pr:`1809`)
	- chore: use utf-8 encoding with read_text (:pr:`1817`)
	- chore: map internal exception classes to setuptools (:pr:`1866`)

#)  New or improved hooks for:
	- hooks: split more hooks in a separate module (:pr:`1790`)
	- hooks: add support for matplotlib 3.7 (:pr:`1791`)
	- hooks: improved hook for pytorch (:pr:`1804`)
	- fix: add tcl8 directory to bases and fix tkinter hooks (:pr:`1812`)
	- hooks: improved hook for matplotlib 3.7 work with bdist_msi (:pr:`1815`)
	- fix: matplotlib hooks (:pr:`1818`, :pr:`1819`)
	- hooks: pyside6/pyqt6 - fix svg and pdf, docs, modules (:pr:`1827`)
	- hooks: pyside6 - check for conda (:pr:`1828`)
	- hooks: include a qt.conf for pyqt6-webengine to work (:pr:`1829`)
	- hooks: include a qt.conf for pyside2-webengine to work (:pr:`1832`)
	- hooks: add new qt plugins based on the docs (:pr:`1835`)
	- hooks: add pyimagej and jpype (:pr:`1842`)
	- hooks: add librosa and lazy_loader hooks (:pr:`1856`)
	- hooks: numpy can be used in conda-forge without mkl [windows] (:pr:`1867`)
	- hooks: add pyreadstat (:pr:`1883`)

#)  Linux:
	- fix: use latest manylinux release to fix tkinter in Python 3.11 (:pr:`1830`)
	- fix: setuptools is unbundled on Gentoo (:pr:`1864`)

#)  Windows:
	- windows: fix file version with four elements (:pr:`1772`)
	- windows: fix error using CX_FREEZE_STAMP=pywin32 (:pr:`1773`)
	- windows: put all msvcr dlls in build_exe top directory (:pr:`1780`)
	- fix: copy all top dependencies [windows,conda] (:pr:`1799`)
	- fix: copy all top dependencies [mingw] (:pr:`1859`)

#)  Documentation:
	- docs: improve options documentation and fix typos (:pr:`1805`)

#)  Improvements/Refactor/Bugfix:
	- Revert "commands: accepts space-delimited string lists" (:pr:`1768`)
	- freezer: fix importerror when using 'path' option (:pr:`1785`)
	- Check that parent directory exists before writing to file (:pr:`1793`)
	- fix: parse namespace packages as packages in zip options (:pr:`1820`)
	- fix: restore build-exe option of build command (now deprecated) (:pr:`1823`)
	- Fix code for year 2038 (:pr:`1860`)
	- fix: ignore recursion into .git subdirectories (:pr:`1884`)

#)  Project:
	- Declare support for setuptools 67.x (:pr:`1782`)
	- Use CodeQL tools for scanning (:pr:`1766`)
	- Use bump2version tag_name (:pr:`1769`)
	- Upgrade pre-commit tools (:pr:`1774`)
	- freezer: pylint ready (:pr:`1781`)
	- dependabot: add package-ecosystem for pip (:pr:`1792`)
	- chore: use ruff (:pr:`1798`, :pr:`1800`, :pr:`1801`, :pr:`1802`, :pr:`1803`, :pr:`1836`)
	- chore: change Makefile to call pylint separated of others tools (:pr:`1807`)
	- chore: update python dependencies (:pr:`1808`, :pr:`1822`)
	- chore: add python version to dependabot (:pr:`1810`)
	- chore: use code_object_replace_function if possible (:pr:`1816`)
	- chore: normalize filename and use map (:pr:`1839`)
	- chore: Generate coverage report (:pr:`1843`)

Version 6.14 (January 2023)
---------------------------

#)  New or improved hooks for:
	- hooks: Add charset_normalizer (:pr:`1758`)
	- hooks: Add shapely (:pr:`1725`)
	- hooks: Add sklearn hook (:pr:`1715`)
	- hooks: Add pytorch (:pr:`1720`)
	- hooks: Update scipy hook (:pr:`1716`)
	- hooks: fix sqlite3 hook in python embed (:pr:`1707`)

#)  Linux:
	- Support to build musllinux wheels (:pr:`1687`)
	- project: Improve patchelf dependency specification (:pr:`1722`)

#)  Windows:
	- startup: Do not limit PATH (revert #1659 partially), limit dll search path (:pr:`1675`)
	- Ignore pylint error for deprecated module msilib (:pr:`1682`)
	- Update to cx_Logging 3.1 and remove hacks for previous version (:pr:`1688`)
	- [windows] Compile base executables with generic names depending on cache_tag (:pr:`1712`)
	- [windows] build-wheel: maintain base executables on git (:pr:`1713`)
	- [windows] build-wheel: fix git rm (use --ignore-unmatch instead) (:pr:`1714`)
	- [windows] build-wheel: fix git branch (:pr:`1717`)
	- [windows] setup: optional compilation in editable mode (:pr:`1718`)

#)  Documentation:
	- pin sphinx to 5.3.0 (:pr:`1691`)
	- docs: fix typo (:pr:`1697`)
	- doc: Add keywords for setup() and reorganize read order (:pr:`1728`)
	- Update copyright year (:pr:`1749`)
	- docs: use 'furo' theme for sphinx (:pr:`1750`)
	- doc: cleanup after use of furo theme (:pr:`1755`)
	- doc: improve documentation about setup script (:pr:`1756`)
	- project and doc: tweak formatting and ordering (:pr:`1762`)
	- Small fixes in code and documentation (:pr:`1738`)

#)  Improvements/Refactor/Bugfix:
	- Include copy of cx_Freeze license with frozen applications (:pr:`1672`)
	- license: move update_frozen_license to a pre-commit (:pr:`1676`)
	- Move OS constants to _compat module (:pr:`1709`)
	- install: run() method needs to exist (:pr:`1747`)
	- Fix the subclassing of internal commands (regression introduced in #1746) (:pr:`1759`)
	- commands: accepts space-delimited string lists (:pr:`1761`)

#)  Project:
	- Support Python 3.11 and set it as default in CI (:pr:`1681`)
	- Drop python 3.6 (:pr:`1670`)
	- Drop the external dependency on importlib-metadata (:pr:`1692`)
	- Drop the external dependency on packaging (:pr:`1730`)
	- Python type hints - upgrade syntax (:pr:`1703`)
	- Cleanup (:pr:`1760`)
	- setup: move metadata to pyproject.toml (setuptools 61+) (:pr:`1677`)
	- pre-commit: fix files that trigger the hook (:pr:`1690`)
	- Update pre-commit dependencies (:pr:`1693`)
	- update dev dependencies (:pr:`1701`)
	- project: add/fix urls (:pr:`1708`)
	- build-wheel: add missing sdist files (:pr:`1711`)
	- dist: Use another approach to export DistributionMetadata (:pr:`1726`)
	- build: setuptools has 'build' command since v62.4.0 (:pr:`1729`)
	- dist: Use setuptools plugins to extend Distribution instead of subclassing (:pr:`1733`)
	- Use setuptools Distribution directly (:pr:`1736`)
	- Add build_exe as subcommand of setuptools build (plugin) (:pr:`1737`)
	- Add/update commands (provisional) and minor tweaks (:pr:`1746`)
	- Add dependabot (:pr:`1752`)
	- Declare support for setuptools 66.0 (:pr:`1753`)
	- Ignore build time error (:pr:`1754`)

#)  Samples:
	- samples: Add simple samples using pyproject.toml and setup.cfg (:pr:`1757`)

Version 6.13 (October 2022)
---------------------------

#)  New or improved hooks for:
	- hooks: Add hooks for PyQt6 (6.3.1 and 6.4.0) (:pr:`1664`)
	- hooks: support for new pyside6 6.4.0 (:pr:`1642`)
	- hooks: support for PySide6 6.4.0 on MSYS2 (:pr:`1655`)

#)  Windows:
	- Fix the filename of .msi file generated by bdist_msi. (:pr:`1591`)
	- Improvements related to bdist_msi --target_name (:pr:`1648`)
	- initscripts: Separate the code needed by windows and mingw and fix the path usage. (:pr:`1652`)
	- Fix missing dlls in build root directory [mingw] (:pr:`1653`)
	- Ensure python3.dll is loaded in some python versions (bpo-29778) (:pr:`1657`)
	- Fix dependency target to work better with MSYS2 (:pr:`1658`)
	- startup: limit the PATH in all windows environments (:pr:`1659`)
	- setup: Fix python compatibility, especially on Windows (:pr:`1656`)
	- parser: lief >= 0.12 is required [windows] (:pr:`1661`)

#)  Samples:
	- samples: fix demo scripts for pythonnet 3 (:pr:`1643`)
	- samples: Add samples for PyQt6 and add readme to some qt samples (:pr:`1663`)

#)  Improvements/Refactor/Bugfix:
	- Refactor ci/requirements.py (:pr:`1644`)
	- tests: add mores tests for bdist_msi (:pr:`1646`)
	- Do not translate newlines (generate identical file across OS) (:pr:`1645`)
	- Fix warning and test docs. (:pr:`1647`)
	- Monkey patch setuptools sandbox to get a better run_setup (:pr:`1649`)
	- tests: cleanup files and directories created (:pr:`1650`)
	- use os.fspath() instead of str() (:pr:`1660`)

Version 6.12 (October 2022)
---------------------------

#)  Linux:
	- Support Linux binary wheel for arm64 (:pr:`1539`)

#)  macOS:
	- darwintools: fix bug in the processing of certain dynamic library references (:pr:`1521`)
	- darwintools: Further clean-up of path resolver code. (:pr:`1529`)
	- Make various errors in darwintools show a warning, rather than terminating freeze (:pr:`1593`)

#)  Windows:
	- freezer: Fix dependency target to avoid duplicates [windows] (:pr:`1623`)
	- Call InitializePython from Service_Main instead of wmain. (:pr:`1572`)
	- bdist_msi: sort options (:pr:`1519`)
	- bdist_msi: Fix unnecessary 'running egg_info' (:pr:`1520`)
	- bdist_msi: Fix target-name and target-version (:pr:`1524`)

#)  New or improved hooks for:
	- Improve tkinter hook to work on all OS (:pr:`1526`)
	- hooks: add hook for orjson (:pr:`1606`)
	- hooks: Ensure include_files only if file exists. (:pr:`1627`)
	- hooks: Add hook for tokenizers (:pr:`1628`)
	- hooks: only bcrypt < 4.0 requires cffi (:pr:`1607`)
	- hooks: update cryptography hook (:pr:`1608`)
	- hooks: bcrypt and cryptography hooks must work with msys2 (:pr:`1609`)
	- qt hooks: Put pyqt5 and pyside2 hooks in separate modules (:pr:`1531`)
	- qt hooks: New pyside6 hooks (:pr:`1533`)
	- qt hooks: fix qthooks imports/exports and add an optional debug mode (:pr:`1551`)
	- qt hooks: Add PyQt5/Pyside2/PySide6 hooks for QtDesigner module (:pr:`1552`)
	- qt hooks: Rewrite pyqt hooks to query Qt Library paths instead of guessing (:pr:`1555`)
	- qt hooks: Restructures qt hooks into subpackages for easier troubleshooting. (:pr:`1561`)
	- qt hooks: set some default paths and fix copies (:pr:`1565`)
	- qt hooks: add resources to PySide2 hooks to work on more environments (:pr:`1566`)
	- qt hooks: extend copy_qt_files to fix pyqtweb (:pr:`1568`)
	- qt hooks: a fix for conda-forge linux (pyside2) (:pr:`1585`)
	- qt hooks: fix the location of auxiliary files of webengine (pyqt5) (:pr:`1586`)
	- Improve opencv-python hook (:pr:`1536`)
	- Improve opencv-python hook on macos (:pr:`1538`)
	- Improve opencv hook for conda linux (:pr:`1556`)
	- Support msys2 in opencv-python hooks and use optimized mode (:pr:`1601`)
	- Restore PyYaml hook (:pr:`1542`)
	- Support for pythonnet 3.0 (:pr:`1600`)
	- hooks: Refactor as a subpackage (:pr:`1528`)
	- hooks: Put numpy hook in separate module (:pr:`1532`)
	- hooks: split Crypto hook in a separate module (:pr:`1602`)
	- hooks: split scipy hook in a separate module (:pr:`1603`)

#)  Samples:
	- samples: Add orjson sample (:pr:`1605`)
	- samples: pyqt5, pyside2 and pyside6 in optimized mode (:pr:`1587`)
	- New pyqt5 simplebrowser sample (adapted from pyside2 sample) (:pr:`1567`)
	- Use pyside6 example simplebrowser as sample (:pr:`1543`)
	- New opencv-python sample (:pr:`1535`)
	- Use the same tkinter sample as used in python (:pr:`1525`)
	- samples: add PhotoImage to tkinter (:pr:`1581`)
	- samples: adapt qt samples to use get_qt_plugins_paths (:pr:`1636`)

#)  Improvements/Refactor/Bugfix:
	- fix setuptools 61+ package discovery and other fixes for 62+ (:pr:`1545`)
	- fix setup to work with setuptools 64.x and 65.x (:pr:`1588`)
	- importlib-metadata >= 4.12.0 raise ValueError instead of returning None (:pr:`1625`)
	- Fixed ValueError / importlib_metadata problem (:pr:`1630`)
	- Fix readthedocs for 6.11
	- pin sphinx 5.0.1 and fix the support for it (:pr:`1512`)
	- update issue template (:pr:`1515`)
	- update dev dependencies (:pr:`1516`)
	- module: Fix .dist-info with subdirectories (:pr:`1514`)
	- Add parse as pylint-ready module (:pr:`1527`)
	- Remove deprecated options in build_exe and bdist_mac (:pr:`1544`)
	- Requires permanent use of lief package on windows (:pr:`1547`)
	- Add a workaround to compile with --no-lto if LTO linking fails (:pr:`1549`)
	- Fix a warning compiling with gcc 12.1 (:pr:`1550`)
	- finder: extend _base_hooks to include hooks in directories (:pr:`1557`)
	- update dev dependencies (:pr:`1558`)
	- setup: use find_packages and include_package_data for simplicity (:pr:`1559`)
	- samples: move to root (:pr:`1560`)
	- finder: extend include_file_as_module to include submodule (:pr:`1562`)
	- bases and initscripts: lowercase to remove pylint invalid-name (:pr:`1563`)
	- Update dev dependencies (:pr:`1584`)
	- tweak the bdist_rpm test (:pr:`1596`)
	- Add test for cx_Freeze.command.bdist_msi (:pr:`1597`)
	- freezer: copy package data using _copy_files to correctly parse dependencies (:pr:`1610`)
	- Improve makefile (:pr:`1619`)
	- Update dev dependencies (:pr:`1620`)
	- Cleanup to support/test with python 3.11b3 (:pr:`1518`)
	- freezer: use internal _create_directory (create the parents, verbose) (:pr:`1635`)

#)  Documentation:
	- Fixed a broken link in documentation (:pr:`1618`)
	- Improved documentation of initial_target_dir option on bdist_msi. (:pr:`1614`)
	- Add FAQ item for big installations (:pr:`1583`)

Version 6.11 (June 2022)
---------------------------

#)  Main Improvements:
	- First step to support static libpython (:pr:`1414`)
	- Set the path to search for modules, and fix the path for built-in modules (:pr:`1419`)
	- New release process relies on bump2version (:pr:`1365`)
	- Improve code to cache dist-info files and convert egg-info to dist-info (:pr:`1367`)
	- Compile base executables with generic names depending on SOABI (:pr:`1393`)
	- Add CI with a pre-commit file (:pr:`1368`)
	- Introduce tests in the GitHub CI (:pr:`1381`)
	- Get rid of some calls to deprecated module distutils (:pr:`1445`)
	- Borrow bdist_rpm from python 3.10 (:pr:`1446`)
	- Borrow bdist_msi from python 3.8 (:pr:`1447`)
	- pin setuptools to a range that works (:pr:`1453`)

#)  Linux:
	- Support for using embedded manylinux static libraries (:pr:`1504`)
	- Fix symlinks to avoid duplicate the target (:pr:`1424`)
	- Fix incorrect default bin path includes (:pr:`1425`)

#)  macOS:
	- Support for using macos static libraries (:pr:`1505`)

#)  Windows:
	- Convert PEP440 version scheme to windows scheme (:pr:`1392`)
	- Lief 0.12 supports delay_imports (:pr:`1426`)
	- LIEF 0.12 supports Python 3.10 (:pr:`1433`)

#)  New or improved hooks for:
	- Added additional hooks for the Qt sqldrivers and styles plugins. (:pr:`1371`)
	- Fix hooks for PySide2 5.15.2.1 (:pr:`1396`)
	- Optimizing and adding some Qt hooks (:pr:`1398`)
	- Use pathlib in qt hooks to always use posix paths as qt does (:pr:`1399`)
	- Add hooks for Pyside2.QtWebEngine* (and pyqtwebengine) (:pr:`1479`)

#)  Samples:
	- Add PySide6 sample (:pr:`1442`)
	- Use pyside2 example simplebrowser as sample (:pr:`1478`)

#)  Improvements/Refactor/Bugfix:
	- Minor tweaks with black (:pr:`1364`)
	- Run isort over the code base (:pr:`1366`)
	- Fixes some errors found by pylint (:pr:`1369`)
	- Fix requirements (:pr:`1373`)
	- Build in isolated mode for python 3.6-3.9 (:pr:`1374`)
	- Fix pre-commit configuration (:pr:`1375`)
	- Skip isort in imports_sample test to fix errors (:pr:`1383`)
	- Update MANIFEST.in and Makefile (:pr:`1391`)
	- Fix the default module name in IncludeFile (:pr:`1400`)
	- pin sphinx to 4.4.0 and fix the support for it (:pr:`1401`)
	- Fix some requirements and versions (:pr:`1402`)
	- Use blacken-docs for python code blocks in the docs (:pr:`1403`)
	- Fix a test after #1402 (:pr:`1404`)
	- Use sphinx rdt theme and minor tweaks (:pr:`1405`)
	- Use new build option in rdt to use py39 (:pr:`1406`)
	- Add pre-commit-sphinx (:pr:`1407`)
	- Add pip-tools pre-commit and enable setup-cfg-fmt (:pr:`1411`)
	- Use Path in setup (:pr:`1412`)
	- Use a self made requirements sync instead of piptools (:pr:`1413`)
	- Add cached_property (and a compatible function) for planned use (:pr:`1417`)
	- readme: To install the latest development build (:pr:`1418`)
	- finder: refactor load_module (:pr:`1420`)
	- The built-in modules are determined based on the cx_Freeze build (:pr:`1421`)
	- Some changes to satisfy the linters (:pr:`1422`)
	- Enable flake8 in pre-commit (:pr:`1423`)
	- Enable flake8 in samples (:pr:`1427`)
	- Bump black from 22.1.0 to 22.3.0 (:pr:`1428`)
	- Enable flake8 in tests (:pr:`1429`)
	- Enable pylint (limited to tests) (:pr:`1430`)
	- Update python dependencies (:pr:`1432`)
	- freezer: refactor to 'consider using with' (:pr:`1434`)
	- finder: use pep8 names (and enable pylint for it) (:pr:`1435`)
	- hooks: fixes docstrings and other lint warnings (:pr:`1436`)
	- hooks: new utility function copy_qt_data (:pr:`1437`)
	- hooks: use function attribute to avoid a pylint warning (:pr:`1438`)
	- hooks and setup are ready to pylint (:pr:`1439`)
	- More configuration to pylint (:pr:`1440`)
	- Fix the main docstring for some modules (:pr:`1441`)
	- Two more modules are ready for pylint. (:pr:`1443`)
	- Add cli and dist as pylint-ready modules (:pr:`1444`)
	- bdist_rpm: Make code style suitable for use in cx_Freeze (:pr:`1448`)
	- bdist_rpm: merge the code to make a unique class (:pr:`1449`)
	- bdist_msi: convert to utf8, apply pyupgrade, black and isort (:pr:`1452`)
	- Declare the new subpackage cx_Freeze.command (:pr:`1451`)
	- bdist_msi: get rid of distutils (:pr:`1454`)
	- bdist_msi: Pass pylint and flake8 (:pr:`1455`)
	- initscripts: pylint ready (:pr:`1456`)
	- bdist_rpm: condicional import (:pr:`1457`)
	- bdist_msi: move all the code to the command subpackage (:pr:`1458`)
	- Document the new code layout (:pr:`1459`)
	- Fix pylint configuration (:pr:`1460`)
	- bdist_mac: move macdist to new name and fix lint errors (:pr:`1461`)
	- bdist_*: fix some pylint invalid-name (:pr:`1462`)
	- Tests: enable a test by platform (:pr:`1463`)
	- build,install: move these commands to the command subpackage (:pr:`1464`)
	- build_exe: move this command to the command subpackage (:pr:`1465`)
	- install_exe: move this command to the command subpackage (:pr:`1466`)
	- install: suppress known deprecation (:pr:`1467`)
	- build: merge the code from distutils to the Build class (:pr:`1468`)
	- The python used to compile and to build is always the same [conda] (:pr:`1469`)
	- build: minor tweaks (:pr:`1471`)
	- pre-commit autoupdate and minor tweaks with pylint (:pr:`1472`)
	- Move setup() and refactor to avoid a future circular import in Freezer (:pr:`1473`)
	- setup: more pylint (:pr:`1474`)
	- Using a trick to get around a dependency on distutils. (:pr:`1475`)
	- CI in one file and cache pip dependencies (:pr:`1476`)
	- tests: Add test for build command (:pr:`1477`)
	- build_exe: fix a bug in the build_exe option (:pr:`1480`)
	- bdist_msi: move user_options to main code, excluding unused options (:pr:`1481`)
	- tests: add find_spec test (and remove similar sample) (:pr:`1482`)
	- Extend setuptools.sandbox.run_setup to work with cx_Freeze setup(). (:pr:`1484`)
	- tests: support for tests using Path (:pr:`1485`)
	- tests: add plist_items test (and remove similar sample) (:pr:`1486`)
	- tests: remove a no longer supported method (:pr:`1487`)
	- tests: add a test for bdist_rpm (:pr:`1488`)
	- pre-commit: fix pyupgrade configuration (:pr:`1489`)
	- doc: Enable text wrapping in table cells using rdt_theme (:pr:`1496`)
	- Update issue templates (:pr:`1507`)
	- update dev dependencies (:pr:`1508`)


Version 6.10 (January 2022)
---------------------------

#)  Improvements:
	- Implements Parser interface to create an abstraction to parse binary
	  files (:pr:`1313`)
	- Implements basic PEParser interface (:pr:`1314`)
	- Helper to create and return a Path-like temporary directory
	  (:pr:`1338`)
	- Use build and tweak requirements (:pr:`1343`)
	- Add a basic pyproject.toml for build and tools (:pr:`1355`)

#)  Refactor and bugfix for all systems:
	- importlib.metadata is no longer provisional in Python 3.10 (:pr:`1316`)
	- Add a new _compat module (:pr:`1317`)
	- Prioritize importlib_metadata in versions lower than 3.10 (:pr:`1353`)
	- Fix an overwrite of silent variable in parser (:pr:`1322`)
	- Copy top dependencies only once (:pr:`1336`, :issue:`1304`,
	  :issue:`1333`)
	- Change the place to set version and set new year (:pr:`1350`)
	- Add more files to the source distribution (:pr:`1349`)
	- Minor tweaks in setup.cfg and add a missing version.py (:pr:`1351`)
	- Avoid error when cx_Freeze.util is not build yet (:pr:`1352`)
	- Use helper TemporaryPath in module (:pr:`1354`)

#)  Linux:
	- Implements ELFParser interface merging patchelf (:pr:`1315`)
	- Use PyPI patchelf rather than installed by OS (:pr:`1341`)

#)  Windows:
	- Drop references to shlwapi.dll on Windows to improve performance
	  (:pr:`1318`)
	- Use the dlltool provided in the same directory as gendef (:pr:`1319`)
	- Update manifest.txt to match python.manifest (:pr:`1320`)
	- Search dlls in sys.path, then in the path [windows] (:pr:`1323`)
	- Use PySys_SetArgvEx in windows too. (:pr:`1324`)
	- Add lief as dependency for windows (:pr:`1325`)
	- Support Application Manifests in Windows (:pr:`1326`, :issue:`385`,
	  :issue:`997`, :issue:`1305`)
	- Creates a manifest for an application that will request elevation
	  (:pr:`1327`, :issue:`1188`)
	- Ignore when lief is not available/installed, like in MSYS2 (:pr:`1328`)
	- util: style changes (:pr:`1329`)
	- Support Path in BeginUpdateResource and fix UpdateResource (:pr:`1330`)
	- Move version stamp to winversioninfo module (:pr:`1331`)
	- Add a simple test to winversioninfo (:pr:`1332`)
	- Implement version stamp [windows][experimental] (:pr:`1334`)
	- Workaround a bug in lief with utf-8 filenames [windows] (:pr:`1339`)
	- Use lief to detect dependencies [windows][experimental] (:pr:`1344`,
	  :issue:`665`)

#)  Samples:
	- Extend the 'icon' sample to use an admin manifest (:pr:`1340`)

#)  Documentation:
	- Documentation for manifest and uac-admin options (:pr:`1337`)
	- Update docs for patchelf (:pr:`1342`)


Version 6.9 (December 2021)
---------------------------

#)  Improvements:
	- Extend Module.in_file_system to support an optimized mode (:pr:`1301`)

#)  Refactor and bugfix for all systems:
	- Fix Implicit Namespace Packages (:pr:`1290`, :issue:`1276`)
	- Extend the support for vendored subpackages (:pr:`1294`)
	- Common: Prevent memory leaks on fail (:pr:`1245`)
	- Merge dis._unpack_opargs into scan_code to be able to fix a bug in py310
	  (:pr:`1306`)
	- Fix some print and f-string (:pr:`1246`)
	- fixing enumerations (:pr:`1263`)
	- Fixes for the existing nose tests (:pr:`1234`)
	- Generate `dev-requirements.txt` + improve readme for contributors wanting
	  to run tests (:pr:`1224`)
	- Convert existing tests to pytest + increase coverage (:pr:`1255`)

#)  Linux:
	- Fix relative path in dependencies, detected in miniconda linux
	  (:pr:`1258`)
	- Create symlinks in the target (:pr:`1292`, :issue:`750`)

#)  macOS:
	- fix bugs in certain subprocess calls (:pr:`1260`)
	- Apply ad-hoc signature to modified libraries (:pr:`1251`)

#)  Windows:
	- Set REINSTALLMODE to force installing same-version executables
	  (:pr:`1252`, :issue:`1250`)

#)  New or improved hooks for:
	- ctypes/libffi (:pr:`1279`)
	- flask-compress (:pr:`1295`, :issue:`1273`)
	- opencv-python (:pr:`1278`, :issue:`1275`)
	- PyQt5 hooks (:pr:`1302`, :issue:`1261`)
	- PySide2 - Linux only (:pr:`1302`)
	- sentry-sdk modules (:pr:`1282`)

#)  Samples:
	- Update PyQt5 sample (:pr:`1307`)

#)  Documentation:
	- Update the FAQ (:pr:`1247`)
	- Update msi doc (:pr:`1248`)
	- fade to black (:pr:`1291`)
	- docs: new item in faq (:pr:`1298`)
	- docs: open external links in a tab (:pr:`1299`)
	- prepare to release with python 3.10 support (:pr:`1308`)


Version 6.8 (September 2021)
----------------------------

#)  Improvements:
	- Support pathlib in ModuleFinder (:pr:`1153`)
	- Use Path in Module.file (:pr:`1158`)
	- Use Path in _replace_paths_in_code (:pr:`1159`)
	- Use Path in Module.path (:pr:`1160`)
	- Convert code in hooks to use Path (:pr:`1161`)
	- Use path.iterdir to simplify a code block (:pr:`1162`)
	- Use Path in executable module (:pr:`1163`)
	- Use Path in ModuleFinder.zip_includes (:pr:`1164`)
	- Use Path in process_path_specs (:pr:`1167`)
	- Use Path in Freezer include_files and zip_includes (:pr:`1168`)
	- Use Path in Freezer.targetdir and some related code (:pr:`1169`)
	- Use Path in Freezer._copy_file and almost remaining related code
	  (:pr:`1172`)
	- Use Path in Executable icon and shortcut_dir (:pr:`1173`)
	- Use Set[Path] in dependent_files (:pr:`1215`)
	- Use subprocess (:pr:`1214`)
	- Add more options to cxfreeze script and tweak the docs (:pr:`1174`)

#)  Refactor and bugfix for all systems:
	- Remove unused and unnecessary code (:pr:`1142`)
	- Add some old modules to exclude list (:pr:`1149`)
	- Fix a last minute change and tweak docstrings (:pr:`1154`)
	- Include files (from a directory) is ignoring the exclude dependencies
	  option (:pr:`1216`)
	- Add more typing to freeze (:pr:`1218`)
	- Create permanent cx_Freeze/bases (:pr:`1227`)
	- Make Freezer.targetdir a property to improve a bit (:pr:`1170`)
	- Code analysis, pep8, f-string (:pr:`1177`)
	- Complementary fixes (:pr:`1179`)
	- Use setuptools instead distutils a bit more (:pr:`1195`)

#)  Linux:
	- Fix py39 in ArchLinux using lto (in a different way than mac)
	  (:pr:`1146`, :issue:`1132`)
	- Patchelf calls supports Path type (:pr:`1178`)
	- Use Path (relative_to and parts) to rewrite the fix rpaths (:pr:`1181`)
	- Complementary patch to #1181 (:pr:`1201`)
	- Fix for Miniconda python in linux (:pr:`1219`)
	- Implement Patchelf.get_needed (still based on ldd) (:pr:`1220`)
	- Implement Patchelf.is_elf to optimize get_needed (:pr:`1221`)
	- Fix dependency target and rpath settings (:pr:`1223`)
	- Patchelf needs permission to write
	  (:pr:`1232`, :issue:`1171`, :issue:`1197`)
	- Disable strip with build --debug [linux] (:pr:`1235`, :issue:`1194`)

#)  macOS:
	- Use Path in darwintools and some pep8 (:pr:`1222`)
	- Fix MachORef in macdist and add-on tweaks to #1222 (:pr:`1229`)

#)  Windows:
	- Fix compatibility with msys2 python 3.9.6 (:pr:`1182`)
	- LLVM dlltool only supports generating an import library (:pr:`1187`)
	- Normalize paths at startup for MSYS2 python (:pr:`1193`)
	- Disable delay load to avoid 'Segmentation fault' in mingw 32 bits
	  (:pr:`1217`)
	- Support Path as parameter for some functions in C (:pr:`1225`)
	- Add a stub interface for util module (:pr:`1226`)
	- Recursing into directories to search for load order files (:pr:`1200`)
	- Fix program files folder for msi using mingw and some tweaks
	  (:pr:`1236`)

#)  New or improved hooks for:
	- _cffi_backend (cffi) (:pr:`1150`)
	- googleapiclient (:pr:`1151`, :issue:`1147`)
	- PyQt5 hooks (:pr:`1148`, :pr:`1155`, :pr:`1156`, :issue:`631`,
	  :issue:`846`, :issue:`972`, :issue:`1119`)
	- PySide2 (:pr:`1183`)
	- tzdata, zoneinfo and backports.zoneinfo
	  (:pr:`1198`, :pr:`1204`, :pr:`1208`)
	- pyzmq (:pr:`1199`)
	- numpy+mkl in conda (:pr:`1205`)

#)  Samples:
	- Fix code of some samples (:pr:`1145`)
	- Remove outdated sample (:pr:`1157`)
	- Improve sample to support pyzmq < 20 and timeout (:pr:`1190`)
	- Tweak pyqt5 and pyside2 samples (:pr:`1180`)
	- Improve PyQt5 and PySide2 samples (:pr:`1192`)

#)  Documentation:
	- Make distutils help and documentation more in line with cxfreeze script
	  (:pr:`1175`)
	- Update distutils build_exe help in docs (:pr:`1176`)
	- Remove distutils references in main docs (:pr:`1196`)
	- Better explain the miniconda installation (:pr:`1209`)
	- Minor updates to docs (:pr:`1230`)


Version 6.7 (July 2021)
-----------------------

#)  Improvements, refactor and bugfix for all systems:
	- Implemented multi levels for build_exe silent option (:pr:`883`)
	- Corrected silent_level to default to 0 (to agree with documentation) (:pr:`1046`)
	- Split up Freezer object (:pr:`1035`)
	- Ignores nonexistent files in dist-info (:pr:`1038`, :issue:`1034`)
	- Use setuptools build_ext to compile base executables and with names that dependes on python version and platform (:pr:`1054`)
	- Use sysconfig and others instead of some distutils modules (:pr:`1055`)
	- Handle the pre-copy task with the _pre_copy_hook method in the freezer (:pr:`1069`)
	- New method to handle platform dependent resources in the freezer (:pr:`1070`)
	- Minor tweaks to tidy up the code (:pr:`1079`)
	- Use wchar if possible. (:pr:`1080`)
	- Create cx_Freeze/bases if it doesn't exist (:pr:`1082`)
	- Use option blocks in the docs and add command line help from commands (:pr:`1097`)
	- Use a valid example in docs (:pr:`1098`)
	- Cleanup versionchanged; limit to 6.0+ (:pr:`1099`)
	- Improve the text of build_exe bin_* (:pr:`1100`)
	- Use of some Sphinx features to organize a bit (:pr:`1102`, :pr:`1138`, :pr:`1139`)
	- Implement Freeze._default_bin_path_includes for all platforms (:pr:`1108`)
	- Move some code to startup to unify the use of environ (:pr:`1112`)
	- Small changes to resolve code warnings (:pr:`1122`)
	- New method Module.update_distribution to update the cached distribution for the frozen executable (:pr:`1123`)
	- Implement DistributionCache.from_name (:pr:`1135`)
	- Use of black and pyupgrade (:pr:`1056`, :pr:`1085`, :pr:`1086`, :pr:`1086`, :pr:`1057`)
	- Use pep8 names in private functions in freezer (:pr:`1068`)
#)  Linux:
	- Fix the support for unix-like systems (:pr:`1067`, :issue:`1061`)
	- check in advance whether the dependency should be copied to avoid changing the rpath unnecessarily. (:pr:`1091`, :issue:`1048`)
	- Fix issue with strip in bdist_rpm (:pr:`1092`, :issue:`1048`)
	- Improve installation docs for linux (:pr:`1095`)
	- Fix a buffer overflow introduced in :pr:`872` (:pr:`1047`)
	- Fix another flaw introduced in :pr:`872` (:pr:`1111`)
	- Fix regression introduced in :pr:`995` (and (:pr:`985`)) (:pr:`1090`, :issue:`1029`)
#)  macOS:
	- Added CFBundlePackageType and NSHighResolutionCapable by default to Info.plist of Darwin bundles (:pr:`1031`, :issue:`239`)
#)  Windows:
	- Transform filename to msilib.Binary for binary data (:pr:`1024`, :issue:`1019`)
	- Add extension registration on Windows (:pr:`1032`)
	- Support for icons with non-ascii names (:pr:`1066`)
	- New C function to update the PE checksum (or fix it in case it is zero) (:pr:`1071`, :issue:`315`, :issue:`1059`)
	- Use setuptools command to install a include file (:pr:`1072`)
	- Fix the support for non-ascii names in windows (:pr:`1077`, :issue:`835`)
	- PyEval_InitThreads is unnecessary in py37+ and is deprecated in py39 (:pr:`1081`)
	- Set working directory in the Desktop shortcut (:pr:`1083`, :issue:`48`, :issue:`623`)
	- Improve documentation about bdist_msi (:pr:`1084`, :issue:`48`)
#)  New or improved hooks for:
	- pydantic (:pr:`1074`, :issue:`1052`)
	- scikit-image (skimage) (:pr:`1104`, :issue:`1101`)
	- plotly (:pr:`1105`, :issue:`1101`)
	- scipy (versions 1.6.3 to 1.7.0) (:pr:`1106`, :pr:`1134`, :issue:`1101`, :issue:`1129`)
	- numpy and numpy+mkl (versions 1.19.5 to 1.21.0) (:pr:`1113`, :pr:`1125`, :issue:`739`, :issue:`1110`)
	- six (:pr:`1115`)
	- hdfdict, h5py_wrapper and pytest-runner (:pr:`1116`, :pr:`1124`, :issue:`1118`)
#)  Samples:
	- pydantic (:pr:`1074`)
	- pythonnet-demo (python.NET sample based on it's demo) (:pr:`1088`, :issue:`1049`)

Version 6.6 (April 2021)
------------------------

#)  Improvements:
	- Enable python -m cx_Freeze syntax (:pr:`899`)
	- Standardize InitializePython on all platforms. (:pr:`872`)
	- Store a copy of cached dist-info (:pr:`958`)
	- Suppress additional output if --silent has been set. (:pr:`830`)
	- Only copy a file if should copy a file (:pr:`995`, :issue:`256`)
	- Refactor cache dist-info files to be extended (:pr:`957`)
	- Remove subfolders belonging to excluded modules (:pr:`922`)
#)  Linux:
	- Implements a new Patchelf interface for patching ELF files (:pr:`966`)
	- Improve the resolution of dependencies [Linux] (:pr:`967`)
	- Use -rpath explicitly (:pr:`940`)
#)  macOS:
	- Another way to detected the use of LTO (:pr:`895`)
	- Failed to create DMG file (applications_shortcut=True`) (:pr:`927`, :issue:`925`)
	- Fix plistlib.load call in macdist [py39] (:pr:`926`, :issue:`924`)
	- Improvements to dependency resolution on Darwin (:pr:`887`)
	- Tweak to only print warning if attempting to copy two mach-o files to the same location.  Only the first file used. (:pr:`915`, :issue:`913`)
#)  Windows:
	- Avoid duplicates of libpythonXX.so and pythonXX.ddl (:pr:`978`)
	- Rebirth of --include-msvcr - real support for vcruntime dlls [windows] (:pr:`973`, :issue:`367`)
	- Set lib directory as default for dll search [windows] (:pr:`1000`)
	- Speedup compiling on windows (:pr:`993`)
	- Support for delay load [mingw] (:pr:`1002`)
	- Support for delay load [windows] (:pr:`1001`)
	- Update to cx_Logging 3.0 (:pr:`909`, :pr:`994`, :pr:`996`, :pr:`998`, :pr:`1012`)
	- Use the delay load to compile Win32Service (:pr:`1003`)
#)  New or improved hooks for:
	- llvmlite (:pr:`1016`)
	- matplotlib (:pr:`971`)
	- mkl-service (:pr:`975`)
	- numpy (:pr:`970`, :pr:`968`)
	- pandas (:pr:`969`)
	- pycountry (:pr:`956`)
	- pyodbc (:pr:`1018`)
	- pyqtgraph (:pr:`1015`)
	- pyzmq 22 (:pr:`953`)
#)  Samples:
	- Add sample for pycountry (:pr:`955`)
	- Add sample for pyzmq (:pr:`954`)
	- Update the service sample and build (:pr:`886`)
	- Update PySide2 sample (:pr:`1011`)
	- Tweak samples (:pr:`888`)
#)  Bugfixes:
	- Force encoding of generated files to utf-8 (:pr:`1005`, :issue:`989`)
	- cx_Logging as submodule (:pr:`874`, :issue:`866`)
	- Avoid the __main__ module from pip wheel (:pr:`894`, :issue:`891`)
	- Fix regression introduced in PR #857 (:pr:`878`, :issue:`875`)
	- Fix typo (:pr:`877`, :issue:`866`)
	- Fix the pillow sample (:pr:`876`)
	- Fix the docs (:pr:`870`)
	- Fix regression introduced in #978 (:pr:`1010`)
	- Standardizes the target directory Freezer (and cxfreeze`) (:pr:`999`)
	- Fix regression introduced in PR #973 (:pr:`976`)
	- Fix PATH for anaconda/miniconda (:pr:`974`)
	- Starts freezing in a clean directory (:pr:`965`)
	- Fix a regression introduced in #798 (:pr:`945`, :issue:`932`)
	- fix regressions introduced in #843 (:pr:`920`, :issue:`919`)
	- Some packages use a directory with vendored modules (:pr:`906`, :issue:`900`)
	- IncludeModule has priority over ExcludeModule (:pr:`904`)
	- Better error checks (:pr:`902`)
	- Support for executable names that may not be valid identifiers (:pr:`889`, :issue:`884`)
	- Accept file without extension as source file to be backwards compatible (:pr:`893`)
#)  Refactor:
	- Update readme (:pr:`1022`)
	- Update installation docs (:pr:`1021`)
	- Modify cxfreeze script a bit (:pr:`1009`)
	- Restructure ConstantModule (:pr:`1004`)
	- Invert the assignment to create a new list (:pr:`987`)
	- Refactor Freezer init (:pr:`985`)
	- New module exception (:pr:`984`)
	- Separates the freezer module classes (:pr:`983`)
	- Update code style in Modules (:pr:`982`)
	- build docs in build dir at project's root (:pr:`981`)
	- Minor update to code style (:pr:`980`)
	- update faq a bit (:pr:`977`)
	- Cleanup freezer copy file method (:pr:`964`)
	- Typo (:pr:`962`)
	- Change detection order and tweak formatting (:pr:`961`)
	- Refactor Module class attributes (:pr:`960`)
	- Fade to black (:pr:`946`, :pr:`1020`)
	- Distribute samples only with source code (:pr:`941`)
	- Add badges (:pr:`944`)
	- Revise docs a bit  (:pr:`943`)
	- Update in the docs the use of main branch (:pr:`942`)
	- remove unused files (:pr:`910`)
	- Update build-wheel (:pr:`903`)
	- Revert previous commit and fix the ident only (:pr:`882`)
	- Fix potential errors (:pr:`881`)
	- Code analysis (:pr:`880`)

Version 6.5 (January 2021)
---------------------------

#)  Improvements:
	- Refactor ModuleFinder to use importlib.machinery (:pr:`811`)
	- Executable target_name now has support for names with version (:pr:`857`)
	- The name of the target executable can be modified after the build
	  (:pr:`858`, :issue:`703`)
	- Use codeType.replace when in py38+ (optimized) (:pr:`836`)
	- Use a configuration file for Read the Docs (:pr:`818`)
	- Modernize code (Type annotation, PEP8, black, refactor)
	  (:pr:`815`, :pr:`832`, :pr:`837`, :pr:`838`, :pr:`839`,
	  :pr:`840`, :pr:`841`, :pr:`842`, :pr:`843`, :pr:`859`,
	  :pr:`860`, :pr:`861`, :pr:`864`, :pr:`865`, :pr:`868`)
#)  Windows:
	- Check if icon is valid
	  (:issue:`856`, :pr:`851`, :issue:`824`, :issue:`379`)
	- Warning about python from Windows Store (:pr:`867`, :issue:`856`)
#)  macOS:
	- Implemented a "plist_items" option on bdist_mac command (:pr:`827`)
	- Remove deprecated methods in macdist (:pr:`810`)
	- Fix a regression for macOS (:pr:`816`, :issue:`809`)
	- Fix a bug using macOS on Github Actions (:pr:`812`)
	- Marked rpath-lib-folder option as depreciated. (:pr:`834`)
#)  New or improved hooks for:
	- cryptography (:pr:`817`, :issue:`814`)
	- google.cloud.storage (:pr:`821`)
	- matplotlib (:pr:`807`, :issue:`805`)
	- pygments (:pr:`863`, :issue:`862`)
	- zoneinfo/tzdata (and backports.zoneinfo) (:pr:`854`)
#)  Samples:
	- Better pytz sample (:pr:`852`)
	- Sample for new library zoneinfo (py39) (:pr:`853`)
	- Sample to demonstrate the use a valid and an invalid icon (:pr:`850`)
#)  Bugfixes:
	- cx_Freeze.__version__ should be the package version
	  (:pr:`806`, :issue:`804`)
	- pin importlib_metadata to >=3.1.1 (:pr:`819`, :pr:`820`, :pr:`822`)
	- Correct test failures when initializing ModuleFinder (:pr:`833`)


Version 6.4 (November 2020)
---------------------------

#)  Improvements:
	- Improved the resolution of dependencies in darwin MachO files (:pr:`590`)
	- Documentation (:pr:`783`, :pr:`796`)
	- Release using GitHub Actions CI/CD workflows (:pr:`797`)
	- Apply pyupgrade (:pr:`801`)
	- Modernize code (Type annotation, PEP8, black, refactor, cleanup)
	  (:pr:`785`, :pr:`776`, :pr:`314`, :pr:`787`, :pr:`784`,
	  :pr:`786`, :pr:`788`, :pr:`789`, :pr:`793`, :pr:`794`,
	  :pr:`780`, :pr:`795`, :pr:`799`, :pr:`800`, :pr:`790`,
	  :pr:`798`)
#)  New or improved hooks for:
	- PyQt5 (:pr:`718`, :pr:`791`)
#)  Samples:
	- Added a sample to illustrate problem with importlib.util.find_spec
	  (:pr:`735`)
	- Sample for bdist_msi, summary_data option (:pr:`775`)
	- README for some samples; remove requirements.txt to avoid to be
	  interpreted by some sites as the requirements of cx_Freeze (:pr:`802`)
#)  Bugfixes:
	- Cause MSI file to be released at the end of bdist_msi command (:pr:`781`)


Version 6.3 (October 2020)
--------------------------

#)  Improvements:
	- Improve metadata using importlib.metadata (:pr:`697`)
	- New options in ``cxfreeze`` script; documentation updated (:pr:`742`)
	- The command line parser was rewritten and modernised using argparse
	  (:pr:`741`)
	- Documentation (:pr:`740`, :pr:`722`, :pr:`720`)
	- Cleanups (:pr:`766`, :pr:`746`, :pr:`744`, :pr:`743`,
	  :pr:`736`, :pr:`726`, :pr:`724`, :pr:`721`, :pr:`712`)
#)  New or improved hooks for:
	- google.cloud.storage (:pr:`708`)
	- google.crc32c (:pr:`737`)
	- matplotlib and numpy (:pr:`695`, :issue:`692`)
	- scipy (:pr:`725`)
	- sysconfig (:pr:`727`, :pr:`715`)
	- tensorflow (:pr:`710`)
#)  Linux:
	- Improve copy dependent files relative to source module file (:pr:`704`)
#)  Windows:
	- Check if upgrade-code is valid and document the valid format
	  (:pr:`711`, :issue:`585`)
	- Improve Windows GUID documentation (:pr:`749`)
	- Added option to bdist_msi to specify information for msi summary
	  information stream (:pr:`760`)
#)  macOS:
	- Fix the syspath for some version of python on macOS
	  (:pr:`719`, :issue:`667`)
#)  Samples:
	- Add pyside2 sample (:pr:`664`)
	- A sample for testing PyQt5 included in zip package (:pr:`717`)
	- Add pandas sample (:pr:`709`)
	- Added sample code to show the use of ConstantsModule / BUILD_CONSTANTS
	  (:pr:`729`)
#)  Bugfixes:
	- Ensure the copy of default python libraries in all platforms
	  (:pr:`706`, :issue:`701`)
	- Remove warning 'Distutils was imported before Setuptools'
	  (:pr:`694`, :issue:`693`)
	- Fix the use of compress and desambiguate the use of stat (:pr:`738`)
	- Small fix to handle a build constant that includes a "=" symbol
	  (:pr:`728`)
	- Fix issue when module.file is None (:pr:`707`)
	- Fix detect namespaces in py35 (:pr:`700`)
	- Set python initialization flags prior to Py_SetPath call to avoid
	  warnings (:pr:`751`)


Version 6.2 (July 2020)
-----------------------

#)  New or improved hooks for:
	- aiofiles (:pr:`600`)
	- babel (:pr:`577`)
	- bcrypt (:pr:`583`, :issue:`581`)
	- certifi (:pr:`690`)
	- cffi.cparser (:pr:`603`)
	- ctypes (for MSYS2 mingw) (:pr:`565`)
	- matplotlib (:pr:`574`, :issue:`569`)
	- pikepdf (:pr:`604`)
	- lxml (:pr:`604`)
	- pycryptodome (:pr:`602`)
	- pygments (:pr:`604`)
	- pkg_resources (:pr:`584`, :issue:`579`)
	- pytest (:pr:`617`)
	- setuptools (:pr:`608`)
	- uvloop (:pr:`689`)
#)  Linux:
	- Pass command line arguments in current locale (:pr:`645`, :issue:`611`)
#)  Windows:
	- Fixed multiprocessing pickling errors (:pr:`622`, :issue:`539`, :issue:`402`, :issue:`403`, :issue:`231`, :issue:`536`)
	- Ensure the copy of default python libraries (:pr:`640`)
	- Replace deprecated functions that will be removed in py4 - win32gui (:pr:`649`)
	- Exclude Tkinter from loaded modules (:pr:`576`, :issue:`567`)
	- Fixed "no module named 'scipy.spatial.cKDTree'" (:pr:`626`, :issue:`233`)
	- Fixed "no module named 'multiprocessing.pool'" (:pr:`627`, :issue:`353`)
	- Download cx_Logging to build Win32Service.exe when building from sources (:pr:`650`, :issue:`519`)
#)  macOS:
	- Fixing modification of PATH for single user install (:pr:`614`, :issue:`613`)
	- Make needed dirs when using include_resources (:pr:`633`)
	- Check for Mach-O using byte strings to allow case of non unicode chars (:pr:`635`)
	- Copy references from /usr/local (:pr:`648`)
#)  Documentation
	- Update doc and faq (:pr:`564`, :pr:`663`, :pr:`688`)
	- Initial work to be pep8 compliant (:pr:`572`, :pr:`582`)
#)  Misc
	- Fixed bug in ``cxfreeze`` script introduced in 6.1 (:issue:`560`).
	- Remove old packages/modules names, do not report as missing (:pr:`605`)
	- Better support for MSYS2 and Anaconda3 (:pr:`642`)
	- Support python 3.5.2 and up (:pr:`606`)
	- Support metadata to use by pkg_resources (:pr:`608`)
	- New common function rebuild_code_object to be reusable (:pr:`629`)
	- Fix optimize option in python 3.8 (:pr:`641`)
	- Add --include-files option to ``cxfreeze`` script (:pr:`647`)
	- Replace the value of __package__ directly in the code (:pr:`651`)
	- Eliminate exclusion of ``dbm`` module since it is in Python 3 (:pr:`662`, :issue:`660`)
	- Detect namespace packages (:pr:`669`, :pr:`668`)
	- Installing from source requires setuptools (:pr:`687`)
	- Remove PyUnicode_FromUnicode (:pr:`673`)

Version 6.1 (January 2020)
--------------------------

#)  Added support for Python 3.8 (:pr:`545`, :pr:`556`).
#)  Added support for ``python setup.py develop`` (:pr:`502`).
#)  Use ``console_scripts`` in ``entry_points`` so that the commands
    ``cxfreeze`` and ``cxfreeze-quickstart`` run on Windows without the need
    for running a postinstall script (:pr:`511`).
#)  Added support for switching from per-user to per-machine installations on
    Windows (:pr:`507`).
#)  Fix installation if ``AlwaysInstallElevated`` policy is set on Windows
    (:pr:`533`).
#)  Updated default dependencies for Python 3 on Windows (:pr:`505`).
#)  Removed unused code (:pr:`549`).
#)  The default dependencies are now always copied into the lib folder instead
    of into the directory where the executable resides on Linux
    (:pr:`518`).
#)  Dependent files are now copied to the same relative directory as their
    location in the source on Linux (:pr:`494`).
#)  Added tests for commonly used packages like ``cryptography``, ``pillow``,
    ``sqlite``, ``pytz``, ``ctypes`` and ``distutils``
    (:pr:`508`, :pr:`537`, :pr:`546`, :pr:`555`, :pr:`557`).
#)  Fix regression with DLL dependencies introduced in 6.0 by :pr:`492`
    due to case differences (:pr:`512`).
#)  Fix regression with dependent files introduced in 6.0 by :pr:`297`
    for platforms other than macOS (:pr:`516`).
#)  The version of cx_Freeze is now defined in one place (:pr:`552`).
#)  Eliminate exclusion of ``gestalt`` module on platforms other than macOS
    since it exists outside of macOS.
#)  Improved hooks for ``sqlite3`` (:pr:`509`), ``cryptography``, and
    ``tkinter`` (:pr:`559`).
#)  Added hook for ``pytz`` (:pr:`554`).
#)  Improved hook infrastructure, permitting hooks to add constants that can
    be examined at runtime, determine whether a module is going to be stored in
    the file system and include files in the zip file.
#)  Improved documentation (:pr:`510`).


Version 6.0 (August 2019)
-------------------------

#)  Corrected support for Python 3.7 (:pr:`395`).
#)  Use importlib and other Python 3 improvements
    (:pr:`484`, :pr:`485`, :pr:`486`, :pr:`490`).
#)  Fixed issue with @rpath causing file copy errors on macOS (:pr:`307`).
#)  Replaced file() with open() and use context manager to ensure the file
    handle is closed and deleted (:pr:`348`).
#)  Corrected invalid version handling in bdist_msi (:pr:`349`, :issue:`340`).
#)  Corrected hook for clr module (:pr:`397`, :pr:`444`).
#)  Corrected documentation for compress option (:pr:`358`).
#)  Ensure that the pythoncom and pywintypes DLLs are found in the lib
    directory and not in the base directory (:issue:`332`).
#)  Always copy dependent files to root directory on macOS (:pr:`365`).
#)  Skip self referencing archive on macOS (:pr:`364`, :issue:`304`).
#)  Include doc directory in source distribution (:pr:`394`, :issue:`376`).
#)  Force msilib module to be reloaded in order to allow for the generation of
    multiple MSI packages in a single session (:pr:`419`).
#)  Added hook for PyQt5.QtPrintSupport module (:pr:`401`).
#)  Added ability to include an icon on the add/remove program window that pops
    up during installation (:pr:`387`).
#)  Prevent spurious errors from being printed during building on macOS by
    checking to see that a file is a Mach-O binary before adding it to the list
    of files it is checking the reference of (:pr:`342`, :issue:`268`).
#)  Avoid otool bug on macOS Yosemite (:pr:`297`, :issue:`292`).
#)  Added ability to specify environment variables that should be created when
    an MSI package is installed (:pr:`266`).
#)  Added support for including resources in an app bundle for macOS
    (:pr:`423`).
#)  Added absolute reference path option for macOS packages (:pr:`424`).
#)  Added CFBundle identifier for macOS packages (:pr:`427`, :issue:`426`).
#)  Added hook for copying SSL DLLs for Python 3.7+ on Windows (:pr:`470`).
#)  Added -municode flag when building on Windows with mingw32 (:pr:`468`).
#)  Added hook for pycparser (:pr:`446`).
#)  Fixed hook for zmq so it doesn't fail when there is no bundled libzmq
    library in the installed pyzmq package (:pr:`442`).
#)  Print error when fetching dependent files fails (:pr:`435`).
#)  Make executable writable before adding the icon
    (:pr:`430`, :issue:`368`).
#)  Dropped support for RPM and MSI packages for cx_Freeze itself since these
    are no longer supported by PyPI.
#)  Fix building console app with mingw32 (:pr:`475`).
#)  Force inclusion of the unicodedata module which is used by the socket
    module, and possibly others (:pr:`476`).
#)  Added hook for asyncio package (:pr:`477`).
#)  Added hook for idna package (:pr:`478`).
#)  Added hook for pkg_resources package (:pr:`481`).
#)  Added hook for gevent (:pr:`495`).
#)  Force .exe extension to be included on Windows, so that the same setup code
    can be used on both Linux and Windows (:pr:`489`).
#)  Added hook for Pillow (:pr:`491`).
#)  Improved hook for tkinter (:pr:`493`).
#)  Avoid attempting to check for dependent files on Windows when the file is
    not an executable or DLL (:pr:`492`).
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
#)  Do not create version resource when version is omitted (:pr:`279`).
#)  Ensure the sqlite3 DLL is loaded in the same directory as the module which
    depends on it (:issue:`296`).
