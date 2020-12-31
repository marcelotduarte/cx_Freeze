"""A simple script to show some values of a font in matplotlib."""

from pathlib import Path
import matplotlib as mpl
from matplotlib.afm import AFM

print("matplotlib datapath:", mpl.get_data_path())
afm_path = Path(mpl.get_data_path(), "fonts", "afm", "ptmr8a.afm")
with afm_path.open("rb") as fh:
    afm = AFM(fh)
print(
    "compare the results with:",
    "https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/afm.py",
)
print(afm.string_width_height("What the heck?"))
print(afm.get_fontname())
print(afm.get_kern_dist("A", "f"))
print(afm.get_kern_dist("A", "y"))
print(afm.get_bbox_char("!"))
