#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NOTE: this code is the sample code found in the openpyxl documentation which
# can be found at https://openpyxl.readthedocs.io/en/default.

from openpyxl import Workbook
wb = Workbook()

# grab the active worksheet
ws = wb.active

# Data can be assigned directly to cells
ws['A1'] = 42

# Rows can also be appended
ws.append([1, 2, 3])

# Python types will automatically be converted
import datetime
ws['A2'] = datetime.datetime.now()

# Save the file
wb.save("sample.xlsx")

