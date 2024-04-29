"""code sample found in the openpyxl documentation."""

# https://openpyxl.readthedocs.io/en/default.

from datetime import datetime, timezone

from openpyxl import Workbook

wb = Workbook()

# grab the active worksheet
ws = wb.active

# Data can be assigned directly to cells
ws["A1"] = 42

# Rows can also be appended
ws.append([1, 2, 3])

# Python types will automatically be converted
ws["A2"] = datetime.now(tz=timezone.utc)

# Save the file
fileName = "sample.xlsx"
wb.save(fileName)
print("Wrote file", fileName)
