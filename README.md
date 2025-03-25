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
| cx\_Freeze/command/bdist\_deb.py      |       65 |       15 |     76.92% |48-52, 57-58, 83-86, 94, 105-114, 120-121 |
| cx\_Freeze/command/bdist\_dmg.py      |      189 |       20 |     89.42% |179-180, 194-198, 217, 222, 230, 263, 289, 291, 372-381 |
| cx\_Freeze/command/bdist\_mac.py      |      209 |      100 |     52.15% |164-168, 189-190, 218-245, 252, 254, 258, 262-284, 293, 304-311, 319, 360, 366, 373-382, 391, 408-422, 442-459, 462-480, 483-485, 488-527 |
| cx\_Freeze/command/bdist\_msi.py      |      424 |       29 |     93.16% |151, 158, 252-253, 676-677, 680, 683, 986-991, 1001-1002, 1005-1013, 1029, 1057-1062, 1065-1070, 1092, 1146, 1150, 1194-1195 |
| cx\_Freeze/command/bdist\_rpm.py      |      233 |       46 |     80.26% |206-210, 215-216, 236-239, 271-275, 279, 299, 319-323, 352-354, 406, 423, 443-444, 452, 455, 458, 461, 507-508, 523, 526-527, 536-550 |
| cx\_Freeze/command/build\_exe.py      |      115 |       48 |     58.26% |161-163, 167-196, 238-243, 247-248, 270, 323-332, 337 |
| cx\_Freeze/command/install.py         |       51 |        0 |    100.00% |           |
| cx\_Freeze/command/install\_exe.py    |       42 |        1 |     97.62% |        76 |
| cx\_Freeze/common.py                  |       67 |       27 |     59.70% |27, 34, 62, 66-67, 69-70, 75-76, 79-80, 98-119 |
| cx\_Freeze/darwintools.py             |      366 |      125 |     65.85% |34, 141, 145-155, 178-180, 184-213, 239-240, 251-256, 259-270, 284, 287-288, 303, 305, 309-320, 347-349, 359-364, 397, 400, 413, 417, 423, 434, 438, 456-471, 475-479, 489-490, 494, 505, 510, 525-529, 550, 569-574, 579, 598-602, 620-624, 649-682 |
| cx\_Freeze/exception.py               |        8 |        0 |    100.00% |           |
| cx\_Freeze/executable.py              |      152 |       12 |     92.11% |95-96, 147-148, 231-235, 237, 246-247, 264-266 |
| cx\_Freeze/finder.py                  |      477 |       47 |     90.15% |140, 142, 163, 232-234, 302, 363-366, 406, 408, 451-454, 456-461, 465-466, 498-501, 539-553, 572, 578, 584, 755, 781, 788, 796-797 |
| cx\_Freeze/freezer.py                 |      761 |      100 |     86.86% |120, 165, 184, 187-188, 193-195, 212-214, 224, 232, 243-245, 299, 316, 337-338, 345-346, 379, 431, 467-472, 474-479, 483-484, 486-487, 538, 547, 563-564, 572-576, 587-592, 732, 739-742, 749-751, 755, 794, 875-877, 888-889, 893-899, 925-930, 935-940, 973-986, 990, 1038, 1084-1087, 1099, 1135-1142, 1154, 1250, 1399, 1403 |
| cx\_Freeze/icons/\_\_init\_\_.py      |        0 |        0 |    100.00% |           |
| cx\_Freeze/module.py                  |      327 |       76 |     76.76% |49, 52-58, 60, 80-99, 108-118, 136, 228, 232, 240-244, 252, 255, 259-260, 268, 278, 283-284, 300-301, 365, 389-393, 404, 421-422, 426-428, 448-461, 473, 475-478 |
| cx\_Freeze/parser.py                  |      291 |       62 |     78.69% |79, 113, 129-130, 171, 180, 195, 207-212, 215, 275, 304, 310-314, 321, 328-329, 333-344, 353-358, 362-369, 375, 381-382, 396-398, 402-403, 412, 420, 428-429, 432-434, 439-440 |
| cx\_Freeze/setupwriter.py             |       78 |       78 |      0.00% |     3-123 |
| cx\_Freeze/winmsvcr.py                |        3 |        0 |    100.00% |           |
| cx\_Freeze/winmsvcr\_repack.py        |      158 |       35 |     77.85% |110-111, 113-114, 133, 139-140, 142-143, 214-215, 219-220, 226, 234, 239-242, 250-251, 262-266, 270-299, 309 |
| cx\_Freeze/winversioninfo.py          |      212 |       42 |     80.19% |56, 61-62, 66-74, 142-143, 217, 219, 222-230, 237-239, 259-260, 262-263, 265-266, 359-378 |
|                             **TOTAL** | **4597** |  **893** | **80.57%** |           |


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