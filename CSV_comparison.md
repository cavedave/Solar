# Comparison: solar.csv vs solar_report_filled.csv

## 1. Are 2023, 2024, 2025 predictions in the data?

**solar.csv**

| Year | Predictions in year columns (2020–2040)                                 | Actually got  |
| ---- | ----------------------------------------------------------------------- | ------------- |
| 2023 | Yes (cur: 2030=5405, 2040=11961; Sus: 2030=6390, 2035=8657, 2040=15296) | Yes (1611.10) |
| 2024 | **No** — all prediction columns empty                                   | Yes (2073.25) |
| 2025 | **No** — all prediction columns empty                                   | Yes (2718)    |

So in **solar.csv**, only **2023** has prediction values in the year columns; 2024 and 2025 have only "Actually got" filled.

**solar_report_filled.csv**

| Year | Predictions in year columns (2020–2050)    | Actually got  |
| ---- | ------------------------------------------ | ------------- |
| 2023 | Yes (cur and sus, 2030/2035/2040/2050)     | Yes (1611.1)  |
| 2024 | Yes (cur and sus, 2030/2035/2040/2050)     | Yes (2073.25) |
| 2025 | Yes (cur only: 2035/2040/2050; 2030 empty) | Yes (2718)    |

So the **2023, 2024, and 2025 predictions you tried to load are present in solar_report_filled.csv**. In **solar.csv** they are only partly there (2023 yes, 2024 and 2025 prediction columns empty).

---

## 2. Do the two CSVs agree in other locations?

**Structure**

- **solar.csv**: 8 columns — `pol`, `Year`, `2020`, `2025`, `2030`, `2035`, `2040`, `Actually got`. No 2050.
- **solar_report_filled.csv**: 9 columns — same plus **2050** before `Actually got`. So the "filled" file has an extra prediction year.

**2023 predictions (where both have values)**

- **cur 2023**
  - solar.csv: 2030 = 5405, 2040 = 11961 (2035 blank).
  - solar_report_filled.csv: 2030 = 4699, 2035 = 7174, 2040 = 9500, 2050 = 12639.
  So **2030 and 2040 do not match** (5405 vs 4699, 11961 vs 9500).
- **sus/Sus 2023**
  - solar.csv: 2030 = 6390, 2035 = 8657, 2040 = 15296.
  - solar_report_filled.csv: 2030 = 5377, 2035 = 8648, 2040 = 11787, 2050 = 16041.
  Again **2030 and 2040 differ**; 2035 is close (8657 vs 8648).

So the two files **do not agree** on 2023 prediction values; the filled file appears to use a different set of numbers (or a different source) for 2023.

**Earlier years (2009–2022)**

- Same rows (pol + Year) and same numeric values; only difference is formatting (integers in solar.csv vs floats like `146.0` in solar_report_filled.csv). So they **agree** on content for those years.

**"Actually got"**

- 2023: 1611.10 vs 1611.1 (same).
- 2024: 2073.25 in both.
- 2025: 2718 in both.
So **Actually got** is consistent.

---

## 3. Other oddities in the data

**solar.csv**

- **pol typo**: row 5 has `curr` instead of `cur` (year 2011).
- **Inconsistent pol spacing/casing**: `cur` (with trailing space), `Sus` vs `cur`; "450" appears with no trailing space.
- **Header spacing**: `pol` and `Year` have trailing spaces.
- **2024/2025**: Only `cur` rows exist; no Sus/sus rows for 2024 or 2025 (same as in filled).

**solar_report_filled.csv**

- **pol normalized**: `cur` and `sus` (lowercase, no trailing spaces); "450" unchanged. So `curr` is effectively fixed to `cur`.
- **2025**: Only `cur` has a row; **no sus row for 2025** (same as solar.csv).
- **2025 cur**: 2030 is empty while 2035, 2040, 2050 are filled — so 2025 predictions are incomplete for the first target year.
- **Trailing blank line**: line 33 is empty.
- **Float formatting**: all numerics as `.0` floats (e.g. 146.0, 248.0).

**Both**

- 2024 and 2025 have only `cur` (no sus) in both files.
- "450" vs "cur/sus": two series (450 and cur/sus) with different coverage (e.g. "450" has no "Actually got" values).

---

## Summary

| Question                              | Answer                                                                                                                                   |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Are 2023/2024/2025 predictions there? | **solar_report_filled.csv**: yes (2023–2025). **solar.csv**: only 2023; 2024 and 2025 prediction columns are empty.                      |
| Do the CSVs agree elsewhere?          | **No** for 2023 prediction values (different numbers). **Yes** for 2009–2022 and for "Actually got" (formatting differs: int vs float).   |
| Oddities                              | pol typo/spacing in solar.csv; no 2050 in solar.csv; no sus 2025 in either; 2025 cur 2030 empty in filled; trailing blank line in filled.  |

---

## Recommended actions

1. **Source of truth**
   - Treat **solar_report_filled.csv** as the canonical dataset if you want 2023–2025 predictions in the year columns and a 2050 column. Use **solar.csv** if you want to keep the original 2023 numbers (5405 / 11961 for cur, etc.) and no 2050.

2. **Backfill 2024 and 2025 into solar.csv (optional)**
   - If solar.csv should match the filled file for 2024/2025, copy the prediction values from solar_report_filled.csv for cur 2024, cur 2025 (and sus 2024 if you add that row) into solar.csv. Add a 2050 column to solar.csv if you want structural parity.

3. **Align 2023 if you want one consistent set**
   - Decide which 2023 predictions are correct (solar.csv’s 5405/11961 vs filled’s 4699/9500 for cur, and similarly for sus). Then either overwrite 2023 in solar_report_filled.csv with solar.csv’s values, or overwrite 2023 in solar.csv with solar_report_filled.csv’s values, and use that file as the single source.

4. **Clean-up**
   - In solar.csv: fix `curr` → `cur`, trim trailing spaces in `pol` and `Year` headers, and normalize `Sus` to `sus` (or `cur`/`Sus` consistently) if you care about consistency.
   - In solar_report_filled.csv: remove the trailing blank line (line 33); optionally fill 2025 cur 2030 if you have a value.
