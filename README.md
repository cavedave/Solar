# Solar PV Generation vs. IEA WEO Projections

This repository contains data and analysis comparing actual solar photovoltaic (PV) generation with projections from the International Energy Agency's (IEA) World Energy Outlook (WEO) reports.

## What This Repository Contains

- **`solar.csv`** - Historical solar PV generation data and WEO projections
- **`code/plot_actual_solar.py`** - Python script to generate the comparison graph
- **`graphs/solar_generation_with_projections.png`** - Generated visualization showing the data

## The Data

The `solar.csv` file contains:
- **Actual solar generation** (TWh) from 2009-2025
- **WEO projections** from various years (2009-2022) for 2020, 2025, 2030, 2035, and 2040
- **Policy scenarios** including "cur" (current policy) and other policy variants

## Key Findings

The analysis reveals an interesting **crossover pattern** in the WEO projections:

- **2020 WEO projections** (starting from 824 TWh in 2020) predict **2,764 TWh for 2030**
- **2021 WEO projections** (starting from 1,023 TWh in 2021) predict **3,492 TWh for 2030**  
- **2022 WEO projections** (starting from 1,293 TWh in 2022) predict **4,011 TWh for 2030**

This creates a counterintuitive situation where earlier predictions from lower starting points are more optimistic than later predictions from higher starting points for the same future years.

## How to Use

### Prerequisites
```bash
pip install pandas matplotlib
```

### Generate the Graph
```bash
python code/plot_actual_solar.py
```

The script will:
1. Load the solar generation data
2. Create a visualization comparing actual vs. projected values
3. Save the graph as `graphs/solar_generation_with_projections.png`

## Graph Features

- **Black line**: Actual solar generation observations
- **Gold lines**: WEO projections from different years
- **X-axis**: Years 2009-2035 (with abbreviated labels for most years, full "2030" and "2035")
- **Y-axis**: Solar generation in TWh (0-6000)
- **Legend**: Positioned at top left inside the graph
- **Attribution**: "by @iamredave" at bottom right

## Data Sources

- **Historical data**: Actual solar PV generation from various sources
- **Projections**: IEA World Energy Outlook reports (2009-2022)
- **Policy scenarios**: Current policy ("cur") projections
- **IEA WEO Reports**: [https://www.oecd.org/en/publications/world-energy-outlook_20725302.html](https://www.oecd.org/en/publications/world-energy-outlook_20725302.html)
- **Ember Energy Monthly Data**: [https://storage.googleapis.com/emb-prod-bkt-publicdata/public-downloads/monthly_full_release_long_format.csv](https://storage.googleapis.com/emb-prod-bkt-publicdata/public-downloads/monthly_full_release_long_format.csv) - Provides 2024 and 2025 solar generation figures

## Notes

**2025 projections are based on the next few months having the same increase from 2024 as the first 7 months had.**

## Repository Structure

```
├── README.md
├── solar.csv
├── code/
│   └── plot_actual_solar.py
└── graphs/
    └── solar_generation_with_projections.png
```

## Contributing

Feel free to submit issues, suggestions, or pull requests to improve the analysis or visualization.

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Created by @iamredave*