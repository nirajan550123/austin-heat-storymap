"""
Recompute the headline correlations from the committed per-neighborhood data.
Confirms the canopy and impervious findings in the README are reproducible.

    python src/verify_correlations.py
"""

import pandas as pd
from scipy import stats

df = pd.read_csv("data/austin_heat_stats.csv")

r_canopy, p_canopy = stats.pearsonr(df["canopy_pct"], df["lst_c"])
r_imperv, p_imperv = stats.pearsonr(df["impervious_pct"], df["lst_c"])

print(f"n = {len(df)} neighborhoods")
print(f"LST vs tree canopy:       r = {r_canopy:+.3f}  (p = {p_canopy:.2e})")
print(f"LST vs impervious surface: r = {r_imperv:+.3f}  (p = {p_imperv:.2e})")
print()
print(f"LST range:    {df.lst_c.min():.1f} to {df.lst_c.max():.1f} C")
print(f"Canopy range: {df.canopy_pct.min():.1f} to {df.canopy_pct.max():.1f} %")
