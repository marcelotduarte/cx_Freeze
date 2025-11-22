# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/marcelotduarte/cx_Freeze/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |      Cover |   Missing |
|-------------------------------------- | -------: | -------: | ---------: | --------: |
| cx\_Freeze/\_\_init\_\_.py            |       53 |        0 |    100.00% |           |
| cx\_Freeze/\_\_main\_\_.py            |        4 |        0 |    100.00% |           |
| cx\_Freeze/\_bytecode.py              |      107 |        3 |     97.20% |72, 83, 117 |
| cx\_Freeze/\_compat.py                |       24 |        0 |    100.00% |           |
| cx\_Freeze/\_license.py               |       27 |        5 |     81.48% |37, 41-42, 47-48 |
| cx\_Freeze/\_pyproject.py             |       20 |        0 |    100.00% |           |
| cx\_Freeze/cli.py                     |      100 |        0 |    100.00% |           |
| cx\_Freeze/command/\_\_init\_\_.py    |        0 |        0 |    100.00% |           |
| cx\_Freeze/command/\_pydialog.py      |       21 |        1 |     95.24% |        85 |
| cx\_Freeze/command/bdist\_appimage.py |      191 |       10 |     94.76% |240, 311, 313, 342-343, 350-352, 357, 376 |
| cx\_Freeze/command/bdist\_deb.py      |       67 |        9 |     86.57% |83-84, 105-114, 120-121 |
| cx\_Freeze/command/bdist\_dmg.py      |      187 |       20 |     89.30% |181-182, 196-200, 219, 224, 232, 264, 290, 292, 373-382 |
| cx\_Freeze/command/bdist\_mac.py      |      209 |      100 |     52.15% |164-168, 189-190, 218-245, 252, 254, 258, 262-284, 293, 304-311, 319, 360, 366, 375-384, 393, 410-424, 444-461, 464-482, 485-487, 490-529 |
| cx\_Freeze/command/bdist\_msi.py      |      454 |       45 |     90.09% |51-52, 63, 163, 170, 264-265, 353-416, 431, 757-758, 761, 764, 1068-1073, 1083-1084, 1087-1095, 1103-1109, 1128, 1137, 1167-1172, 1175-1180, 1202, 1252, 1296-1297, 1307, 1311 |
| cx\_Freeze/command/bdist\_rpm.py      |      234 |       35 |     85.04% |235-238, 318-322, 351-353, 405, 422, 442-443, 451, 454, 457, 460, 506-507, 522, 525-526, 535-549 |
| cx\_Freeze/command/build\_exe.py      |      124 |       43 |     65.32% |164-166, 170-199, 335-344, 349 |
| cx\_Freeze/command/install.py         |       51 |        0 |    100.00% |           |
| cx\_Freeze/command/install\_exe.py    |       42 |        0 |    100.00% |           |
| cx\_Freeze/common.py                  |       38 |        8 |     78.95% |55-56, 58-59, 64-65, 68-69 |
| cx\_Freeze/darwintools.py             |      370 |       95 |     74.32% |145-155, 178-180, 184-213, 239-240, 254-255, 266-269, 302, 308-319, 349, 361-366, 399, 402, 415, 419, 425, 436, 440, 458-473, 477-481, 491-492, 496, 507, 512, 527-531, 552, 571-576, 600-604, 651, 664-670 |
| cx\_Freeze/dep\_parser.py             |      291 |       19 |     93.47% |170, 197-202, 205, 265, 296, 306, 314, 321-322, 388-390, 404, 424-426 |
| cx\_Freeze/exception.py               |        8 |        0 |    100.00% |           |
| cx\_Freeze/executable.py              |      168 |        0 |    100.00% |           |
| cx\_Freeze/finder.py                  |      438 |       23 |     94.75% |127, 129, 150, 220-221, 365, 377-381, 424, 426, 478-479, 483-484, 536-539, 574, 580, 586, 714 |
| cx\_Freeze/freezer.py                 |      770 |       72 |     90.65% |235-237, 255, 266-268, 333, 370-371, 399, 451, 487-492, 494-499, 503-504, 506-507, 749, 836, 917-919, 930-931, 935-941, 947, 951, 958, 967-972, 977-982, 1019, 1025-1026, 1032, 1076, 1122-1125, 1137, 1173-1180, 1192, 1288, 1427-1428, 1437, 1441 |
| cx\_Freeze/module.py                  |      356 |       25 |     92.98% |52-58, 60, 105, 111, 244, 289-290, 294, 313, 318-319, 335-336, 380-382, 403, 413, 465 |
| cx\_Freeze/setupwriter.py             |       78 |       78 |      0.00% |     3-126 |
| cx\_Freeze/winversioninfo.py          |      211 |        6 |     97.16% |56, 142-143, 236-238 |
|                             **TOTAL** | **4643** |  **597** | **87.14%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/marcelotduarte/cx_Freeze/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/marcelotduarte/cx_Freeze/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/marcelotduarte/cx_Freeze/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/marcelotduarte/cx_Freeze/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fmarcelotduarte%2Fcx_Freeze%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/marcelotduarte/cx_Freeze/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.