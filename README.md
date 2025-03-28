# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/marcelotduarte/cx_Freeze/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |      Cover |   Missing |
|-------------------------------------- | -------: | -------: | ---------: | --------: |
| cx\_Freeze/\_\_init\_\_.py            |       52 |        0 |    100.00% |           |
| cx\_Freeze/\_\_main\_\_.py            |        4 |        0 |    100.00% |           |
| cx\_Freeze/\_compat.py                |       17 |        0 |    100.00% |           |
| cx\_Freeze/\_pyproject.py             |       20 |        0 |    100.00% |           |
| cx\_Freeze/bases/\_\_init\_\_.py      |        0 |        0 |    100.00% |           |
| cx\_Freeze/cli.py                     |       99 |        5 |     94.95% |233-236, 250, 262 |
| cx\_Freeze/command/\_\_init\_\_.py    |        0 |        0 |    100.00% |           |
| cx\_Freeze/command/\_pydialog.py      |       21 |        1 |     95.24% |        85 |
| cx\_Freeze/command/bdist\_appimage.py |      156 |       24 |     84.62% |93-97, 114, 120-126, 141-142, 160-168, 181, 186, 211, 269-270, 279-281, 286, 294, 301, 305 |
| cx\_Freeze/command/bdist\_deb.py      |       66 |       15 |     77.27% |50-54, 59-60, 85-88, 96, 107-116, 122-123 |
| cx\_Freeze/command/bdist\_dmg.py      |      189 |       20 |     89.42% |179-180, 194-198, 217, 222, 230, 263, 289, 291, 372-381 |
| cx\_Freeze/command/bdist\_mac.py      |      209 |      100 |     52.15% |164-168, 189-190, 218-245, 252, 254, 258, 262-284, 293, 304-311, 319, 360, 366, 373-382, 391, 408-422, 442-459, 462-480, 483-485, 488-527 |
| cx\_Freeze/command/bdist\_msi.py      |      425 |       29 |     93.18% |153, 160, 254-255, 678-679, 682, 685, 988-993, 1003-1004, 1007-1015, 1031, 1059-1064, 1067-1072, 1094, 1148, 1152, 1194-1195 |
| cx\_Freeze/command/bdist\_rpm.py      |      234 |       46 |     80.34% |208-212, 217-218, 238-241, 273-277, 281, 301, 321-325, 354-356, 408, 425, 445-446, 454, 457, 460, 463, 509-510, 525, 528-529, 538-552 |
| cx\_Freeze/command/build\_exe.py      |      116 |       48 |     58.62% |163-165, 169-198, 240-245, 249-250, 272, 325-334, 339 |
| cx\_Freeze/command/install.py         |       51 |        0 |    100.00% |           |
| cx\_Freeze/command/install\_exe.py    |       42 |        1 |     97.62% |        76 |
| cx\_Freeze/common.py                  |       67 |       27 |     59.70% |27, 34, 62, 66-67, 69-70, 75-76, 79-80, 98-119 |
| cx\_Freeze/darwintools.py             |      366 |      120 |     67.21% |34, 141, 145-155, 178-180, 184-213, 239-240, 251-256, 259-270, 284, 287-288, 303, 305, 309-320, 347-349, 359-364, 397, 400, 413, 417, 423, 434, 438, 456-471, 475-479, 489-490, 494, 505, 510, 550, 569-574, 579, 598-602, 620-624, 649-682 |
| cx\_Freeze/exception.py               |        8 |        0 |    100.00% |           |
| cx\_Freeze/executable.py              |      152 |       12 |     92.11% |95-96, 147-148, 231-235, 237, 246-247, 264-266 |
| cx\_Freeze/finder.py                  |      478 |       47 |     90.17% |142, 144, 165, 234-236, 304, 365-368, 408, 410, 453-456, 458-463, 467-468, 500-503, 541-555, 574, 580, 586, 757, 783, 790, 798-799 |
| cx\_Freeze/freezer.py                 |      761 |       97 |     87.25% |120, 165, 184, 187-188, 193-195, 212-214, 224, 232, 299, 316, 337-338, 345-346, 379, 431, 467-472, 474-479, 483-484, 486-487, 538, 547, 563-564, 572-576, 587-592, 732, 739-742, 749-751, 755, 794, 875-877, 888-889, 893-899, 925-930, 935-940, 973-986, 990, 1038, 1084-1087, 1099, 1135-1142, 1154, 1250, 1399, 1403 |
| cx\_Freeze/icons/\_\_init\_\_.py      |        0 |        0 |    100.00% |           |
| cx\_Freeze/module.py                  |      327 |       76 |     76.76% |49, 52-58, 60, 80-99, 108-118, 136, 228, 232, 240-244, 252, 255, 259-260, 268, 278, 283-284, 300-301, 365, 389-393, 404, 421-422, 426-428, 448-461, 473, 475-478 |
| cx\_Freeze/parser.py                  |      291 |       62 |     78.69% |79, 113, 129-130, 171, 180, 195, 207-212, 215, 275, 304, 310-314, 321, 328-329, 333-344, 353-358, 362-369, 375, 381-382, 396-398, 402-403, 412, 420, 428-429, 432-434, 439-440 |
| cx\_Freeze/setupwriter.py             |       78 |       78 |      0.00% |     3-123 |
| cx\_Freeze/winmsvcr.py                |        3 |        0 |    100.00% |           |
| cx\_Freeze/winmsvcr\_repack.py        |      158 |       35 |     77.85% |110-111, 113-114, 133, 139-140, 142-143, 214-215, 219-220, 226, 234, 239-242, 250-251, 262-266, 270-299, 309 |
| cx\_Freeze/winversioninfo.py          |      212 |       42 |     80.19% |56, 61-62, 66-74, 142-143, 217, 219, 222-230, 237-239, 259-260, 262-263, 265-266, 359-378 |
|                             **TOTAL** | **4602** |  **885** | **80.77%** |           |


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