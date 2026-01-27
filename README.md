# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/marcelotduarte/cx_Freeze/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |      Cover |   Missing |
|-------------------------------------- | -------: | -------: | ---------: | --------: |
| cx\_Freeze/\_\_init\_\_.py            |       58 |        0 |    100.00% |           |
| cx\_Freeze/\_\_main\_\_.py            |        4 |        0 |    100.00% |           |
| cx\_Freeze/\_bytecode.py              |      107 |        3 |     97.20% |72, 83, 117 |
| cx\_Freeze/\_compat.py                |       26 |        0 |    100.00% |           |
| cx\_Freeze/\_license.py               |       27 |        5 |     81.48% |37, 41-42, 47-48 |
| cx\_Freeze/\_pyproject.py             |       20 |        0 |    100.00% |           |
| cx\_Freeze/cli.py                     |      100 |        0 |    100.00% |           |
| cx\_Freeze/command/\_\_init\_\_.py    |        0 |        0 |    100.00% |           |
| cx\_Freeze/command/\_pydialog.py      |       21 |        1 |     95.24% |        85 |
| cx\_Freeze/command/bdist\_appimage.py |      191 |       10 |     94.76% |240, 311, 313, 342-343, 350-352, 357, 376 |
| cx\_Freeze/command/bdist\_deb.py      |       67 |        9 |     86.57% |83-84, 105-114, 120-121 |
| cx\_Freeze/command/bdist\_dmg.py      |      187 |       18 |     90.37% |182-183, 197-201, 232, 264, 290, 292, 373-382 |
| cx\_Freeze/command/bdist\_mac.py      |      208 |       99 |     52.40% |164-168, 189-190, 218-245, 252, 254, 258, 262-284, 293, 304-311, 359, 365, 374-383, 392, 409-423, 443-460, 463-481, 484-486, 489-528 |
| cx\_Freeze/command/bdist\_msi.py      |      447 |       51 |     88.59% |52-53, 64, 215, 222, 314-332, 405-469, 484, 805, 807, 810-811, 814, 817, 1125-1130, 1140-1141, 1144-1152, 1188, 1222-1227, 1230-1235, 1259, 1348-1349, 1359, 1363 |
| cx\_Freeze/command/bdist\_rpm.py      |      234 |       35 |     85.04% |235-238, 318-322, 351-353, 405, 422, 442-443, 451, 454, 457, 460, 506-507, 522, 525-526, 535-549 |
| cx\_Freeze/command/build\_exe.py      |      130 |       43 |     66.92% |164-166, 170-199, 346-355, 360 |
| cx\_Freeze/command/install.py         |       51 |        0 |    100.00% |           |
| cx\_Freeze/command/install\_exe.py    |       42 |        0 |    100.00% |           |
| cx\_Freeze/common.py                  |       38 |        8 |     78.95% |55-56, 58-59, 64-65, 68-69 |
| cx\_Freeze/darwintools.py             |      370 |       90 |     75.68% |145-155, 178-180, 184-213, 239-240, 254-255, 266-269, 302, 308-319, 349, 361-366, 399, 402, 415, 419, 425, 436, 440, 458-473, 477-481, 491-492, 496, 507, 512, 552, 571-576, 600-604, 651, 664-670 |
| cx\_Freeze/dep\_parser.py             |      291 |       19 |     93.47% |170, 197-202, 205, 265, 296, 306, 314, 321-322, 388-390, 404, 424-426 |
| cx\_Freeze/exception.py               |        8 |        0 |    100.00% |           |
| cx\_Freeze/executable.py              |      174 |        0 |    100.00% |           |
| cx\_Freeze/finder.py                  |      439 |       23 |     94.76% |125, 127, 151, 221-222, 366, 378-382, 425, 427, 479-480, 484-485, 537-540, 575, 581, 587, 715 |
| cx\_Freeze/freezer.py                 |      775 |       71 |     90.84% |236-238, 256, 337, 374-375, 403, 455, 491-496, 498-503, 507-508, 510-511, 759, 846, 912-913, 927-929, 940-941, 945-951, 957, 961, 968, 977-982, 987-992, 1029, 1035-1036, 1042, 1086, 1132-1135, 1147, 1183-1190, 1202, 1298, 1437-1438, 1447, 1451 |
| cx\_Freeze/module.py                  |      362 |       25 |     93.09% |52-58, 60, 105, 111, 244, 289-290, 294, 313, 318-319, 341-342, 389-391, 415, 426, 478 |
| cx\_Freeze/setupwriter.py             |       78 |       78 |      0.00% |     3-126 |
| cx\_Freeze/winversioninfo.py          |      211 |        6 |     97.16% |56, 142-143, 236-238 |
| **TOTAL**                             | **4666** |  **594** | **87.27%** |           |


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