# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/marcelotduarte/cx_Freeze/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |      Cover |   Missing |
|-------------------------------------- | -------: | -------: | ---------: | --------: |
| cx\_Freeze/\_\_init\_\_.py            |       67 |        0 |    100.00% |           |
| cx\_Freeze/\_\_main\_\_.py            |        4 |        0 |    100.00% |           |
| cx\_Freeze/\_bytecode.py              |      108 |        3 |     97.22% |75, 86, 121 |
| cx\_Freeze/\_compat.py                |       26 |        0 |    100.00% |           |
| cx\_Freeze/\_license.py               |       28 |        5 |     82.14% |36, 40-41, 46-47 |
| cx\_Freeze/\_metadata.py              |      117 |        7 |     94.02% | 45-50, 52 |
| cx\_Freeze/\_pyproject.py             |       35 |        0 |    100.00% |           |
| cx\_Freeze/cli.py                     |       97 |        0 |    100.00% |           |
| cx\_Freeze/command/\_\_init\_\_.py    |        0 |        0 |    100.00% |           |
| cx\_Freeze/command/\_pydialog.py      |       22 |        1 |     95.45% |       119 |
| cx\_Freeze/command/bdist\_appimage.py |      194 |        9 |     95.36% |251, 324, 326, 355-356, 366-368, 389 |
| cx\_Freeze/command/bdist\_deb.py      |       67 |        9 |     86.57% |87-88, 104-113, 119-120 |
| cx\_Freeze/command/bdist\_dmg.py      |      194 |       18 |     90.72% |188-189, 203-207, 238, 272, 294, 296, 377-386 |
| cx\_Freeze/command/bdist\_mac.py      |      217 |      102 |     53.00% |170-174, 194-195, 225-251, 259, 261, 265, 269-291, 301, 312-319, 371, 377, 386-395, 404, 421-435, 456-473, 476-502, 505-544 |
| cx\_Freeze/command/bdist\_msi.py      |      454 |       56 |     87.67% |56-57, 68, 219, 226, 321-339, 412-478, 493, 824, 826, 829-830, 833, 836, 1140-1145, 1155-1156, 1159-1167, 1206, 1214, 1221, 1223, 1236, 1242-1247, 1250-1255, 1279, 1368-1369, 1379, 1383 |
| cx\_Freeze/command/bdist\_rpm.py      |      241 |       35 |     85.48% |239-242, 326-330, 360-362, 414, 433, 453-454, 462, 465, 468, 471, 517-518, 533, 536-537, 546-560 |
| cx\_Freeze/command/build\_exe.py      |      141 |       43 |     69.50% |169-171, 177-206, 366-375, 380 |
| cx\_Freeze/command/install.py         |       51 |        0 |    100.00% |           |
| cx\_Freeze/command/install\_exe.py    |       43 |        0 |    100.00% |           |
| cx\_Freeze/common.py                  |       38 |        8 |     78.95% |57-58, 63-64, 66-67, 69-70 |
| cx\_Freeze/darwintools.py             |      379 |       96 |     74.67% |151-161, 185-187, 191-215, 243-244, 258-259, 270-273, 306, 312-323, 354, 366-371, 404, 407, 422, 426, 432, 445, 449, 467-483, 488-492, 502-503, 507, 517, 523, 538-542, 563, 582-587, 611-615, 662, 675-681 |
| cx\_Freeze/dep\_parser.py             |      308 |       25 |     91.88% |190, 196, 202, 225-230, 233, 252, 254-256, 298, 329, 339, 347, 354-355, 422-424, 439, 460-462 |
| cx\_Freeze/exception.py               |        8 |        0 |    100.00% |           |
| cx\_Freeze/executable.py              |      176 |        0 |    100.00% |           |
| cx\_Freeze/finder.py                  |      477 |       27 |     94.34% |141, 143, 167, 208, 241-242, 318, 375-378, 390, 402-406, 483, 571-574, 593-594, 624, 630, 636, 671, 783 |
| cx\_Freeze/freezer.py                 |      788 |       76 |     90.36% |238-240, 258, 269-271, 280, 342, 379-380, 410, 462, 498-503, 505-510, 514-515, 517-518, 772, 804, 861, 927-928, 942-944, 955-956, 960-966, 972, 976, 984, 995-1000, 1005-1010, 1047, 1053-1054, 1060, 1104, 1150-1153, 1165, 1202-1209, 1221, 1317, 1459-1460, 1469, 1473 |
| cx\_Freeze/module.py                  |      262 |       19 |     92.75% |85, 89, 136-137, 141, 160, 165-166, 188-189, 235, 238-241, 257, 268, 279, 332 |
| cx\_Freeze/setupwriter.py             |       75 |       75 |      0.00% |     3-124 |
| cx\_Freeze/winversioninfo.py          |      213 |        6 |     97.18% |62, 148-149, 242-244 |
| **TOTAL**                             | **4830** |  **620** | **87.16%** |           |


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