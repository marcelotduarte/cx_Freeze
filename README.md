# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/marcelotduarte/cx_Freeze/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |      Cover |   Missing |
|-------------------------------------- | -------: | -------: | ---------: | --------: |
| cx\_Freeze/\_\_init\_\_.py            |       60 |        0 |    100.00% |           |
| cx\_Freeze/\_\_main\_\_.py            |        4 |        0 |    100.00% |           |
| cx\_Freeze/\_bytecode.py              |      108 |        3 |     97.22% |74, 85, 119 |
| cx\_Freeze/\_compat.py                |       26 |        0 |    100.00% |           |
| cx\_Freeze/\_license.py               |       28 |        5 |     82.14% |36, 40-41, 46-47 |
| cx\_Freeze/\_pyproject.py             |       21 |        0 |    100.00% |           |
| cx\_Freeze/cli.py                     |      100 |        0 |    100.00% |           |
| cx\_Freeze/command/\_\_init\_\_.py    |        0 |        0 |    100.00% |           |
| cx\_Freeze/command/\_pydialog.py      |       21 |        1 |     95.24% |        85 |
| cx\_Freeze/command/bdist\_appimage.py |      194 |        9 |     95.36% |251, 324, 326, 355-356, 363-365, 386 |
| cx\_Freeze/command/bdist\_deb.py      |       64 |        9 |     85.94% |83-84, 100-109, 115-116 |
| cx\_Freeze/command/bdist\_dmg.py      |      194 |       18 |     90.72% |188-189, 203-207, 238, 272, 294, 296, 377-386 |
| cx\_Freeze/command/bdist\_mac.py      |      219 |      103 |     52.97% |169-173, 193-194, 222-248, 255, 257, 261, 265-287, 296, 307-314, 366, 372, 381-390, 399, 416-430, 450-467, 470-492, 495-497, 500-539 |
| cx\_Freeze/command/bdist\_msi.py      |      446 |       51 |     88.57% |52-53, 64, 215, 222, 314-332, 405-469, 484, 805, 807, 810-811, 814, 817, 1125-1130, 1140-1141, 1144-1152, 1188, 1222-1227, 1230-1235, 1259, 1347-1348, 1358, 1362 |
| cx\_Freeze/command/bdist\_rpm.py      |      242 |       35 |     85.54% |236-239, 321-325, 356-358, 409, 428, 448-449, 457, 460, 463, 466, 512-513, 528, 531-532, 541-555 |
| cx\_Freeze/command/build\_exe.py      |      141 |       43 |     69.50% |169-171, 175-204, 364-373, 378 |
| cx\_Freeze/command/install.py         |       51 |        0 |    100.00% |           |
| cx\_Freeze/command/install\_exe.py    |       43 |        0 |    100.00% |           |
| cx\_Freeze/common.py                  |       38 |        8 |     78.95% |56-57, 62-63, 65-66, 68-69 |
| cx\_Freeze/darwintools.py             |      379 |       96 |     74.67% |151-161, 185-187, 191-215, 243-244, 258-259, 270-273, 306, 312-323, 354, 366-371, 404, 407, 422, 426, 432, 445, 449, 467-483, 488-492, 502-503, 507, 517, 523, 538-542, 563, 582-587, 611-615, 662, 675-681 |
| cx\_Freeze/dep\_parser.py             |      296 |       19 |     93.58% |187, 214-219, 222, 286, 317, 327, 335, 342-343, 410-412, 427, 447-449 |
| cx\_Freeze/exception.py               |        8 |        0 |    100.00% |           |
| cx\_Freeze/executable.py              |      176 |        0 |    100.00% |           |
| cx\_Freeze/finder.py                  |      476 |       26 |     94.54% |132, 134, 158, 197, 230-231, 360-363, 375, 387-391, 473, 563-566, 585-586, 615, 621, 627, 661, 767 |
| cx\_Freeze/freezer.py                 |      787 |       81 |     89.71% |237-239, 257, 268-270, 279, 340, 377-378, 406, 458, 494-499, 501-506, 510-511, 513-514, 764, 796, 853, 891-895, 918-919, 933-935, 946-947, 951-957, 963, 967, 975, 986-991, 996-1001, 1038, 1044-1045, 1051, 1095, 1141-1144, 1156, 1193-1200, 1212, 1308, 1450-1451, 1460, 1464 |
| cx\_Freeze/module.py                  |      374 |       27 |     92.78% |56-61, 63, 110, 116, 266, 313-314, 318, 337, 342-343, 365-366, 412, 415-418, 436, 447, 458, 510 |
| cx\_Freeze/setupwriter.py             |       78 |       78 |      0.00% |     3-126 |
| cx\_Freeze/winversioninfo.py          |      213 |        6 |     97.18% |59, 145-146, 239-241 |
| **TOTAL**                             | **4787** |  **618** | **87.09%** |           |


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