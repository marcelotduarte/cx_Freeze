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
| cx\_Freeze/command/bdist\_appimage.py |      156 |       22 |     85.90% |93-97, 114, 120-126, 141-142, 160-168, 211, 269-270, 279-281, 286, 294, 301, 305 |
| cx\_Freeze/command/bdist\_deb.py      |       66 |       17 |     74.24% |50-54, 56-57, 59-60, 85-88, 96, 107-116, 122-123 |
| cx\_Freeze/command/bdist\_dmg.py      |      189 |       20 |     89.42% |179-180, 194-198, 217, 222, 230, 263, 289, 291, 372-381 |
| cx\_Freeze/command/bdist\_mac.py      |      209 |      100 |     52.15% |164-168, 189-190, 218-245, 252, 254, 258, 262-284, 293, 304-311, 319, 360, 366, 373-382, 391, 408-422, 442-459, 462-480, 483-485, 488-527 |
| cx\_Freeze/command/bdist\_msi.py      |      437 |       36 |     91.76% |159, 166, 260-261, 349-412, 427, 753-754, 757, 760, 1064-1069, 1079-1080, 1083-1091, 1107, 1137-1142, 1145-1150, 1172, 1226, 1230, 1272-1273 |
| cx\_Freeze/command/bdist\_rpm.py      |      234 |       46 |     80.34% |208-212, 217-218, 238-241, 273-277, 281, 301, 321-325, 354-356, 408, 425, 445-446, 454, 457, 460, 463, 509-510, 525, 528-529, 538-552 |
| cx\_Freeze/command/build\_exe.py      |      116 |       48 |     58.62% |163-165, 169-198, 240-245, 249-250, 272, 325-334, 339 |
| cx\_Freeze/command/install.py         |       51 |        0 |    100.00% |           |
| cx\_Freeze/command/install\_exe.py    |       42 |        1 |     97.62% |        76 |
| cx\_Freeze/common.py                  |       65 |       12 |     81.54% |30, 58, 62-63, 65-66, 71-72, 75-76, 95, 106 |
| cx\_Freeze/darwintools.py             |      366 |      117 |     68.03% |34, 141, 145-155, 178-180, 184-213, 239-240, 251-256, 259-270, 287-288, 303, 305, 309-320, 347-349, 359-364, 397, 400, 413, 417, 423, 434, 438, 456-471, 475-479, 489-490, 494, 505, 510, 550, 569-574, 598-602, 620-624, 656-682 |
| cx\_Freeze/dep\_parser.py             |      289 |       64 |     77.85% |79, 113, 129-130, 179, 194, 206-211, 214, 222-224, 241-243, 302, 312, 315-317, 320, 327-328, 332-343, 352-357, 361-367, 373, 379-380, 394-396, 400-401, 410, 418, 426-427, 430-432, 437-438 |
| cx\_Freeze/exception.py               |        8 |        0 |    100.00% |           |
| cx\_Freeze/executable.py              |      153 |       14 |     90.85% |79-81, 95-96, 145, 150-151, 234-238, 240, 264-266 |
| cx\_Freeze/finder.py                  |      475 |       34 |     92.84% |142, 144, 165, 235-236, 304, 365-368, 408, 410, 453-456, 458-463, 467-468, 500-503, 547, 574, 580, 586, 781, 795-796 |
| cx\_Freeze/freezer.py                 |      757 |       97 |     87.19% |165, 184, 187-188, 193-195, 212-214, 224, 232, 299, 336-337, 342-343, 376, 428, 464-469, 471-476, 480-481, 483-484, 535, 544, 560-561, 569-573, 584-589, 747-749, 753, 792, 873-875, 886-887, 891-897, 903, 907, 914, 923-928, 933-938, 971-984, 988, 1036, 1082-1085, 1097, 1133-1140, 1152, 1248, 1387-1388, 1397, 1401 |
| cx\_Freeze/icons/\_\_init\_\_.py      |        0 |        0 |    100.00% |           |
| cx\_Freeze/module.py                  |      332 |       58 |     82.53% |52-58, 60, 79-98, 105, 111, 118-128, 235, 245-249, 257, 260, 264-265, 273, 283, 288-289, 305-306, 409, 433, 456-457, 462-465, 478, 480-483 |
| cx\_Freeze/setupwriter.py             |       78 |       78 |      0.00% |     3-123 |
| cx\_Freeze/winmsvcr.py                |        3 |        0 |    100.00% |           |
| cx\_Freeze/winmsvcr\_repack.py        |      158 |       35 |     77.85% |110-111, 113-114, 133, 139-140, 142-143, 214-215, 219-220, 226, 234, 239-242, 250-251, 262-266, 270-299, 309 |
| cx\_Freeze/winversioninfo.py          |      211 |       36 |     82.94% |56, 61-62, 66-74, 142-143, 218, 223-225, 236-238, 258-259, 261-262, 264-265, 358-377 |
|                             **TOTAL** | **4613** |  **836** | **81.88%** |           |


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