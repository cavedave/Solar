# Next steps: add WEO 2026 (launch 19 Nov 2026)

## Add the WEO 2026 predictions
1. Put the report in `WEO/pdfs/` (e.g. `WorldEnergyOutlook2026.pdf`).
2. Find **Annex A, Table A.3a "World electricity sector"** (the Current Policies scenario, if the report still leads with it).
3. Use the **top** "Solar PV" row, which is generation in **TWh**. The lower Solar PV row is capacity in GW. The 2023 and 2024 rows were once taken from the GW row by mistake.
4. Fill in the existing `cur,2026` row in `solar_report_filled.csv` (columns 2030, 2035, 2040, 2050). Keep its `Actually got` value.
5. Save the page: `pdfseparate -f N -l N WEO/pdfs/WorldEnergyOutlook2026.pdf WEO/tmp/weo-2026-pN.pdf`
6. Run `python code/plot_solar_styled.py`. The charts go to `graphs/solar_generation_styled*.png`.

## Actuals (decided 20 Nov 2026: use IEA figures)
- 2024 = 2089 TWh and 2025 = 2723 TWh, both IEA's historical figures from WEO 2026 Table A.3a.
- Ember for comparison: 2024 is about 2127 TWh and 2025 is 2771.6 TWh.

## 2026 actual is an estimate
- `cur,2026` Actually got = 3194.1 TWh. This is IEA's 2025 total × Ember (Jan–Sep 2026 / Jan–Sep 2025) = 2723 × 1.1730.
- The value is listed in `ESTIMATED_YEARS` in `code/plot_solar_styled.py`, so the charts draw it dashed and label it "estimate".
- Replace it with IEA's 2026 figure (WEO 2027) or rescale once Ember has the full year, then remove 2026 from `ESTIMATED_YEARS`.
- The Ember data has moved to: https://files.ember-energy.org/public-downloads/generation/outputs/release_generation_monthly_global.csv
  The README link is out of date. The world solar monthly series is saved in `WEO/ember_world_solar_monthly.csv`.

## Scenario notes
- WEO 2024 has no Current Policies scenario. Table "a" is Stated Policies, so `cur,2024` is really Stated Policies and `sus,2024` is Announced Pledges.
- WEO 2025 brought back Current Policies. Its annex has no 2030 column, so the 2025 line goes straight to 2035.
- The chart footer says "Current Policies" for every year. It may need to say "Current/Stated Policies".
