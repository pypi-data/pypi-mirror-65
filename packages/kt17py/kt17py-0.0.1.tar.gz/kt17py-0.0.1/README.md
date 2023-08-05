# kt17py

A Python wrapper to the FORTRAN code for the KT17 dynamic magnetic field model for Mercury's magnetosphere.

See Korth, H., Johnson, C. L., Philpott, L.,Tsyganenko, N. A., & Anderson, B. J.(2017). A dynamic model of Mercury’s
magnetospheric magnetic field. Geophysical Research Letters, 44. https://doi.org/10.1002/2017GL074699

# How to use

```python
import numpy as np
from kt17py.kt17 import *

kt17 = Kt17(0.39,0.50)
xyz_msm = np.array([[-2.0,0.0,0.5]])
b_msm = kt17.bfield(xyz_msm)
```

# Testing builds

Since kt17py contains Fortran files that need to be compiled before use, the tests are currently run against the version
of kt17py (if any) found on current PYTHONPATH.

```console
python -m unittest tests/kt17.py
```
