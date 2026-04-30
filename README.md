# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/marcelotduarte/cx_Freeze/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |      Cover |   Missing |
|-------------------------------------- | -------: | -------: | ---------: | --------: |
| cx\_Freeze/\_\_init\_\_.py            |       59 |        0 |    100.00% |           |
| cx\_Freeze/\_\_main\_\_.py            |        4 |        0 |    100.00% |           |
| cx\_Freeze/\_bytecode.py              |      107 |        3 |     97.20% |72, 83, 117 |
| cx\_Freeze/\_compat.py                |       26 |        0 |    100.00% |           |
| cx\_Freeze/\_license.py               |       27 |        5 |     81.48% |37, 41-42, 47-48 |
| cx\_Freeze/\_pyproject.py             |       20 |        0 |    100.00% |           |
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
| cx\_Freeze/common.py                  |       38 |        8 |     78.95% |55-56, 58-59, 64-65, 68-69 |
| cx\_Freeze/darwintools.py             |      370 |       95 |     74.32% |145-155, 178-180, 184-213, 239-240, 254-255, 266-269, 302, 308-319, 349, 361-366, 399, 402, 415, 419, 425, 436, 440, 458-473, 477-481, 491-492, 496, 507, 512, 527-531, 552, 571-576, 600-604, 651, 664-670 |
| cx\_Freeze/dep\_parser.py             |      291 |       19 |     93.47% |170, 197-202, 205, 265, 296, 306, 314, 321-322, 388-390, 404, 424-426 |
| cx\_Freeze/exception.py               |        8 |        0 |    100.00% |           |
| cx\_Freeze/executable.py              |      174 |        0 |    100.00% |           |
| cx\_Freeze/finder.py                  |      464 |       22 |     95.26% |130, 132, 156, 226-227, 356-359, 371, 383-387, 555-558, 572-573, 606, 612, 746 |
| cx\_Freeze/freezer.py                 |      774 |       74 |     90.44% |236-238, 256, 267-269, 337, 374-375, 403, 455, 491-496, 498-503, 507-508, 510-511, 761, 848, 914-915, 929-931, 942-943, 947-953, 959, 963, 970, 979-984, 989-994, 1031, 1037-1038, 1044, 1088, 1134-1137, 1149, 1185-1192, 1204, 1300, 1439-1440, 1449, 1453 |
| cx\_Freeze/module.py                  |      365 |       25 |     93.15% |54-60, 62, 107, 113, 251, 296-297, 301, 320, 325-326, 348-349, 396-398, 422, 433, 485 |
| cx\_Freeze/setupwriter.py             |       78 |       78 |      0.00% |     3-126 |
| cx\_Freeze/winversioninfo.py          |      211 |        6 |     97.16% |56, 142-143, 236-238 |
| **TOTAL**                             | **4696** |  **601** | **87.20%** |           |


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