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
| cx\_Freeze/command/bdist\_appimage.py |      189 |        9 |     95.24% |240, 311, 313, 342-343, 350-352, 373 |
| cx\_Freeze/command/bdist\_deb.py      |       63 |        9 |     85.71% |82-83, 99-108, 114-115 |
| cx\_Freeze/command/bdist\_dmg.py      |      192 |       18 |     90.62% |187-188, 202-206, 237, 269, 295, 297, 378-387 |
| cx\_Freeze/command/bdist\_mac.py      |      213 |      100 |     53.05% |168-172, 193-194, 222-248, 255, 257, 261, 265-287, 296, 307-314, 362, 368, 377-386, 395, 412-426, 446-463, 466-484, 487-489, 492-531 |
| cx\_Freeze/command/bdist\_msi.py      |      446 |       51 |     88.57% |52-53, 64, 215, 222, 314-332, 405-469, 484, 805, 807, 810-811, 814, 817, 1125-1130, 1140-1141, 1144-1152, 1188, 1222-1227, 1230-1235, 1259, 1347-1348, 1358, 1362 |
| cx\_Freeze/command/bdist\_rpm.py      |      233 |       35 |     84.98% |235-238, 318-322, 351-353, 402, 419, 439-440, 448, 451, 454, 457, 503-504, 519, 522-523, 532-546 |
| cx\_Freeze/command/build\_exe.py      |      130 |       43 |     66.92% |165-167, 171-200, 347-356, 361 |
| cx\_Freeze/command/install.py         |       51 |        0 |    100.00% |           |
| cx\_Freeze/command/install\_exe.py    |       42 |        0 |    100.00% |           |
| cx\_Freeze/common.py                  |       38 |        8 |     78.95% |56-57, 62-63, 65-66, 68-69 |
| cx\_Freeze/darwintools.py             |      371 |       95 |     74.39% |148-158, 181-183, 187-216, 242-243, 257-258, 269-272, 305, 311-322, 352, 364-369, 402, 405, 418, 422, 428, 439, 443, 461-476, 480-484, 494-495, 499, 510, 515, 530-534, 555, 574-579, 603-607, 654, 667-673 |
| cx\_Freeze/dep\_parser.py             |      296 |       19 |     93.58% |187, 214-219, 222, 286, 317, 327, 335, 342-343, 410-412, 427, 447-449 |
| cx\_Freeze/exception.py               |        8 |        0 |    100.00% |           |
| cx\_Freeze/executable.py              |      176 |        0 |    100.00% |           |
| cx\_Freeze/finder.py                  |      476 |       26 |     94.54% |132, 134, 158, 197, 230-231, 360-363, 375, 387-391, 473, 563-566, 585-586, 615, 621, 627, 661, 767 |
| cx\_Freeze/freezer.py                 |      787 |       81 |     89.71% |237-239, 257, 268-270, 279, 340, 377-378, 406, 458, 494-499, 501-506, 510-511, 513-514, 764, 796, 853, 891-895, 918-919, 933-935, 946-947, 951-957, 963, 967, 975, 986-991, 996-1001, 1038, 1044-1045, 1051, 1095, 1141-1144, 1156, 1193-1200, 1212, 1308, 1450-1451, 1460, 1464 |
| cx\_Freeze/module.py                  |      374 |       27 |     92.78% |56-61, 63, 110, 116, 266, 311-312, 316, 335, 340-341, 363-364, 410, 413-416, 434, 445, 456, 508 |
| cx\_Freeze/setupwriter.py             |       78 |       78 |      0.00% |     3-126 |
| cx\_Freeze/winversioninfo.py          |      211 |        6 |     97.16% |59, 145-146, 239-241 |
| **TOTAL**                             | **4742** |  **614** | **87.05%** |           |


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