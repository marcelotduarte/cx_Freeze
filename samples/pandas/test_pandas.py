from __future__ import annotations

import numpy as np
import pandas as pd

print("numpy version", np.__version__)
print("pandas version", pd.__version__)

a = np.arange(1.0, 10.0).reshape((3, 3)) % 5
np.linalg.det(a)
a @ a
a @ a.T
np.linalg.inv(a)
np.sin(np.exp(a))
np.linalg.svd(a)
np.linalg.eigh(a)

np.unique(np.random.randint(0, 10, 100))
np.sort(np.random.uniform(0, 10, 100))

np.fft.fft(np.exp(2j * np.pi * np.arange(8) / 8))
np.ma.masked_array(np.arange(10), np.random.rand(10) < 0.5).sum()
np.polynomial.Legendre([7, 8, 9]).roots()

df = pd.DataFrame(np.random.random(size=(100, 5)))
corr_mat = df.corr()
mask = np.tril(np.ones_like(corr_mat, dtype=bool), k=-1)
print(corr_mat.where(mask))
