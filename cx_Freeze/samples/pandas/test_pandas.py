import pandas as pd
import numpy as np

print("pandas version", pd.__version__)

df = pd.DataFrame(np.random.random(size=(100, 5)))
corr_mat = df.corr()
mask = np.tril(np.ones_like(corr_mat, dtype=np.bool), k=-1)
print(corr_mat.where(mask))
