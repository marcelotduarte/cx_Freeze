# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/marcelotduarte/cx_Freeze/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |      Cover |   Missing |
|-------------------------------------- | -------: | -------: | ---------: | --------: |
| cx\_Freeze/\_\_init\_\_.py            |       52 |        0 |    100.00% |           |
| cx\_Freeze/\_\_main\_\_.py            |        4 |        0 |    100.00% |           |
| cx\_Freeze/\_compat.py                |       21 |        0 |    100.00% |           |
| cx\_Freeze/\_pyproject.py             |       20 |        0 |    100.00% |           |
| cx\_Freeze/bases/\_\_init\_\_.py      |        0 |        0 |    100.00% |           |
| cx\_Freeze/cli.py                     |      100 |        0 |    100.00% |           |
| cx\_Freeze/command/\_\_init\_\_.py    |        0 |        0 |    100.00% |           |
| cx\_Freeze/command/\_pydialog.py      |       21 |        1 |     95.24% |        85 |
| cx\_Freeze/command/bdist\_appimage.py |      156 |        8 |     94.87% |213, 271-272, 281-283, 288, 307 |
| cx\_Freeze/command/bdist\_deb.py      |       67 |        9 |     86.57% |83-84, 105-114, 120-121 |
| cx\_Freeze/command/bdist\_dmg.py      |      189 |       20 |     89.42% |179-180, 194-198, 217, 222, 230, 263, 289, 291, 372-381 |
| cx\_Freeze/command/bdist\_mac.py      |      209 |      100 |     52.15% |164-168, 189-190, 218-245, 252, 254, 258, 262-284, 293, 304-311, 319, 360, 366, 373-382, 391, 408-422, 442-459, 462-480, 483-485, 488-527 |
| cx\_Freeze/command/bdist\_msi.py      |      437 |       36 |     91.76% |159, 166, 260-261, 349-412, 427, 753-754, 757, 760, 1064-1069, 1079-1080, 1083-1091, 1107, 1137-1142, 1145-1150, 1172, 1226, 1230, 1272-1273 |
| cx\_Freeze/command/bdist\_rpm.py      |      234 |       35 |     85.04% |235-238, 318-322, 351-353, 405, 422, 442-443, 451, 454, 457, 460, 506-507, 522, 525-526, 535-549 |
| cx\_Freeze/command/build\_exe.py      |      117 |       43 |     63.25% |163-165, 169-198, 328-337, 342 |
| cx\_Freeze/command/install.py         |       51 |        0 |    100.00% |           |
| cx\_Freeze/command/install\_exe.py    |       42 |        0 |    100.00% |           |
| cx\_Freeze/common.py                  |       65 |       11 |     83.08% |30, 62-63, 65-66, 71-72, 75-76, 95, 106 |
| cx\_Freeze/darwintools.py             |      366 |      113 |     69.13% |34, 141, 145-155, 178-180, 184-213, 239-240, 251-256, 263-270, 287-288, 303, 309-320, 347-349, 359-364, 397, 400, 413, 417, 423, 434, 438, 456-471, 475-479, 489-490, 494, 505, 510, 550, 569-574, 598-602, 620-624, 649-682 |
| cx\_Freeze/dep\_parser.py             |      295 |       32 |     89.15% |121-122, 171, 186, 198-203, 206, 269, 300, 310, 318, 325-326, 371, 377-378, 392-394, 398-399, 408, 416, 424-425, 428-430, 435-436 |
| cx\_Freeze/exception.py               |        8 |        0 |    100.00% |           |
| cx\_Freeze/executable.py              |      153 |        0 |    100.00% |           |
| cx\_Freeze/finder.py                  |      475 |       23 |     95.16% |142, 144, 165, 235-236, 304, 408, 410, 462-463, 467-468, 500-503, 547, 574, 580, 586, 781, 795-796 |
| cx\_Freeze/freezer.py                 |      760 |       78 |     89.74% |214-216, 226, 234, 301, 338-339, 344-345, 378, 430, 466-471, 473-478, 482-483, 485-486, 794, 875-877, 888-889, 893-899, 905, 909, 916, 925-930, 935-940, 973-986, 990, 1038, 1084-1087, 1099, 1135-1142, 1154, 1250, 1389-1390, 1399, 1403 |
| cx\_Freeze/icons/\_\_init\_\_.py      |        0 |        0 |    100.00% |           |
| cx\_Freeze/module.py                  |      329 |       46 |     86.02% |52-58, 60, 79-98, 105, 111, 118-128, 235, 249, 260, 264-265, 273, 283, 288-289, 305-306, 409, 433 |
| cx\_Freeze/setupwriter.py             |       78 |       78 |      0.00% |     3-123 |
| cx\_Freeze/winmsvcr.py                |        3 |        0 |    100.00% |           |
| cx\_Freeze/winmsvcr\_repack.py        |      158 |       35 |     77.85% |110-111, 113-114, 133, 139-140, 142-143, 214-215, 219-220, 226, 234, 239-242, 250-251, 262-266, 270-299, 309 |
| cx\_Freeze/winversioninfo.py          |      211 |        6 |     97.16% |56, 142-143, 236-238 |
|                             **TOTAL** | **4621** |  **674** | **85.41%** |           |


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