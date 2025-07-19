# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/marcelotduarte/cx_Freeze/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |      Cover |   Missing |
|-------------------------------------- | -------: | -------: | ---------: | --------: |
| cx\_Freeze/\_\_init\_\_.py            |       52 |        0 |    100.00% |           |
| cx\_Freeze/\_\_main\_\_.py            |        4 |        0 |    100.00% |           |
| cx\_Freeze/\_compat.py                |       24 |        0 |    100.00% |           |
| cx\_Freeze/\_pyproject.py             |       20 |        0 |    100.00% |           |
| cx\_Freeze/bases/\_\_init\_\_.py      |        0 |        0 |    100.00% |           |
| cx\_Freeze/cli.py                     |      100 |        0 |    100.00% |           |
| cx\_Freeze/command/\_\_init\_\_.py    |        0 |        0 |    100.00% |           |
| cx\_Freeze/command/\_pydialog.py      |       21 |        1 |     95.24% |        85 |
| cx\_Freeze/command/bdist\_appimage.py |      156 |        8 |     94.87% |214, 272-273, 282-284, 289, 308 |
| cx\_Freeze/command/bdist\_deb.py      |       67 |        9 |     86.57% |83-84, 105-114, 120-121 |
| cx\_Freeze/command/bdist\_dmg.py      |      189 |       20 |     89.42% |179-180, 194-198, 217, 222, 230, 263, 289, 291, 372-381 |
| cx\_Freeze/command/bdist\_mac.py      |      209 |      100 |     52.15% |164-168, 189-190, 218-245, 252, 254, 258, 262-284, 293, 304-311, 319, 360, 366, 375-384, 393, 410-424, 444-461, 464-482, 485-487, 490-529 |
| cx\_Freeze/command/bdist\_msi.py      |      437 |       36 |     91.76% |159, 166, 260-261, 349-412, 427, 753-754, 757, 760, 1064-1069, 1079-1080, 1083-1091, 1107, 1137-1142, 1145-1150, 1172, 1226, 1230, 1272-1273 |
| cx\_Freeze/command/bdist\_rpm.py      |      234 |       35 |     85.04% |235-238, 318-322, 351-353, 405, 422, 442-443, 451, 454, 457, 460, 506-507, 522, 525-526, 535-549 |
| cx\_Freeze/command/build\_exe.py      |      117 |       43 |     63.25% |163-165, 169-198, 328-337, 342 |
| cx\_Freeze/command/install.py         |       51 |        0 |    100.00% |           |
| cx\_Freeze/command/install\_exe.py    |       42 |        0 |    100.00% |           |
| cx\_Freeze/common.py                  |       65 |       25 |     61.54% |30, 62-63, 65-66, 71-72, 75-76, 94-115 |
| cx\_Freeze/darwintools.py             |      370 |      124 |     66.49% |34, 141, 145-155, 178-180, 184-213, 239-240, 251-255, 258-269, 283, 286-287, 302, 304, 308-319, 346-351, 361-366, 399, 402, 415, 419, 425, 436, 440, 458-473, 477-481, 491-492, 496, 507, 512, 552, 571-576, 581, 600-604, 622-626, 651-684 |
| cx\_Freeze/dep\_parser.py             |      293 |       26 |     91.13% |121-122, 166, 172, 181, 193-198, 201, 264, 295, 305, 308-310, 313, 320-321, 387-389, 403, 423-425 |
| cx\_Freeze/exception.py               |        8 |        0 |    100.00% |           |
| cx\_Freeze/executable.py              |      153 |        0 |    100.00% |           |
| cx\_Freeze/finder.py                  |      509 |       57 |     88.80% |143, 145, 166, 235-237, 289-290, 305, 389, 401-405, 448, 450, 502-503, 507-508, 517-520, 527-529, 542, 557-560, 576, 598-612, 631, 637, 643, 819-838, 852-853 |
| cx\_Freeze/freezer.py                 |      770 |       93 |     87.92% |214-216, 226, 234, 301, 338-339, 344-345, 378, 430, 466-471, 473-478, 482-483, 485-486, 674-679, 709-713, 728, 754, 761-764, 815, 909-910, 914-920, 926, 930, 937, 946-951, 956-961, 994-1007, 1011, 1059, 1105-1108, 1120, 1156-1163, 1175, 1271, 1385-1389, 1410-1411, 1420, 1424 |
| cx\_Freeze/icons/\_\_init\_\_.py      |        0 |        0 |    100.00% |           |
| cx\_Freeze/module.py                  |      354 |       46 |     87.01% |52-58, 60, 67, 105, 111, 165-166, 183-186, 241, 272, 283, 287-288, 296, 306, 311-312, 328-329, 333-336, 339, 358-362, 367-368, 373-376, 397, 407, 459 |
| cx\_Freeze/setupwriter.py             |       78 |       78 |      0.00% |     3-126 |
| cx\_Freeze/winmsvcr.py                |        3 |        0 |    100.00% |           |
| cx\_Freeze/winmsvcr\_repack.py        |      158 |       15 |     90.51% |110-111, 113-114, 139-140, 142-143, 241-244, 252-253, 312 |
| cx\_Freeze/winversioninfo.py          |      211 |       10 |     95.26% |56, 142-143, 227-229, 236-238, 382 |
|                             **TOTAL** | **4695** |  **726** | **84.54%** |           |


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