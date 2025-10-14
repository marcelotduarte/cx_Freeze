# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/marcelotduarte/cx_Freeze/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |      Cover |   Missing |
|-------------------------------------- | -------: | -------: | ---------: | --------: |
| cx\_Freeze/\_\_init\_\_.py            |       53 |        0 |    100.00% |           |
| cx\_Freeze/\_\_main\_\_.py            |        4 |        0 |    100.00% |           |
| cx\_Freeze/\_bytecode.py              |       62 |        0 |    100.00% |           |
| cx\_Freeze/\_compat.py                |       24 |        0 |    100.00% |           |
| cx\_Freeze/\_license.py               |       27 |        5 |     81.48% |37, 41-42, 47-48 |
| cx\_Freeze/\_pyproject.py             |       20 |        0 |    100.00% |           |
| cx\_Freeze/cli.py                     |      100 |        0 |    100.00% |           |
| cx\_Freeze/command/\_\_init\_\_.py    |        0 |        0 |    100.00% |           |
| cx\_Freeze/command/\_pydialog.py      |       21 |        1 |     95.24% |        85 |
| cx\_Freeze/command/bdist\_appimage.py |      156 |        8 |     94.87% |214, 272-273, 282-284, 289, 308 |
| cx\_Freeze/command/bdist\_deb.py      |       67 |        9 |     86.57% |83-84, 105-114, 120-121 |
| cx\_Freeze/command/bdist\_dmg.py      |      187 |       20 |     89.30% |181-182, 196-200, 219, 224, 232, 264, 290, 292, 373-382 |
| cx\_Freeze/command/bdist\_mac.py      |      209 |      100 |     52.15% |164-168, 189-190, 218-245, 252, 254, 258, 262-284, 293, 304-311, 319, 360, 366, 375-384, 393, 410-424, 444-461, 464-482, 485-487, 490-529 |
| cx\_Freeze/command/bdist\_msi.py      |      432 |       38 |     91.20% |55-56, 156, 163, 257-258, 346-409, 424, 750-751, 754, 757, 1059-1064, 1074-1075, 1078-1086, 1102, 1132-1137, 1140-1145, 1167, 1221, 1225, 1267-1268 |
| cx\_Freeze/command/bdist\_rpm.py      |      234 |       35 |     85.04% |235-238, 318-322, 351-353, 405, 422, 442-443, 451, 454, 457, 460, 506-507, 522, 525-526, 535-549 |
| cx\_Freeze/command/build\_exe.py      |      124 |       43 |     65.32% |164-166, 170-199, 335-344, 349 |
| cx\_Freeze/command/install.py         |       51 |        0 |    100.00% |           |
| cx\_Freeze/command/install\_exe.py    |       42 |        0 |    100.00% |           |
| cx\_Freeze/common.py                  |       62 |       10 |     83.87% |58-59, 61-62, 67-68, 71-72, 91, 102 |
| cx\_Freeze/darwintools.py             |      370 |       95 |     74.32% |145-155, 178-180, 184-213, 239-240, 254-255, 266-269, 302, 308-319, 349, 361-366, 399, 402, 415, 419, 425, 436, 440, 458-473, 477-481, 491-492, 496, 507, 512, 527-531, 552, 571-576, 600-604, 651, 664-670 |
| cx\_Freeze/dep\_parser.py             |      291 |       21 |     92.78% |122-123, 167, 194-199, 202, 262, 293, 303, 311, 318-319, 385-387, 401, 421-423 |
| cx\_Freeze/exception.py               |        8 |        0 |    100.00% |           |
| cx\_Freeze/executable.py              |      154 |        0 |    100.00% |           |
| cx\_Freeze/finder.py                  |      462 |       24 |     94.81% |128, 130, 151, 221-222, 374, 386-390, 433, 435, 487-488, 492-493, 545-548, 592, 619, 625, 631, 759 |
| cx\_Freeze/freezer.py                 |      770 |       72 |     90.65% |232-234, 252, 263-265, 330, 367-368, 396, 448, 484-489, 491-496, 500-501, 503-504, 746, 833, 914-916, 927-928, 932-938, 944, 948, 955, 964-969, 974-979, 1016, 1022-1023, 1029, 1077, 1123-1126, 1138, 1174-1181, 1193, 1289, 1428-1429, 1438, 1442 |
| cx\_Freeze/module.py                  |      356 |       27 |     92.42% |52-58, 60, 105, 111, 244, 275, 286, 289-290, 294, 313, 318-319, 335-336, 380-382, 403, 413, 465 |
| cx\_Freeze/setupwriter.py             |       78 |       78 |      0.00% |     3-126 |
| cx\_Freeze/winversioninfo.py          |      211 |        6 |     97.16% |56, 142-143, 236-238 |
|                             **TOTAL** | **4575** |  **592** | **87.06%** |           |


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