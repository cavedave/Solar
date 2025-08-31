#!/usr/bin/env python3
"""
Simple script to plot actual solar generation observations with projection lines.
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def plot_actual_solar_with_projections():
    """Plot the actual solar generation observations with projection lines."""
    
    # Load the data
    df = pd.read_csv("solar.csv")
    
    # Clean column names - strip all whitespace
    df.columns = df.columns.str.strip()
    
    # Get the actual observations (remove rows where "Actually got" is NaN)
    actual_data = df[df['Actually got'].notna()].copy()
    
    # Filter for current policy projections (excluding 2023 WEO)
    # Handle both 'cur' and 'Cur' variations, and strip whitespace from pol column
    cur_data = df[(df['pol'].str.strip().str.lower() == 'cur') & (df['Year'] != 2023)]
    
    print("Actual solar generation data:")
    print(actual_data[['Year', 'Actually got']])
    print("\nCur projection data:")
    print(cur_data[['Year', '2020', '2025', '2030', '2035', '2040']])
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Plot the actual observations as a black line with markers
    plt.plot(actual_data['Year'], actual_data['Actually got'], 
             'ko-', linewidth=2, markersize=6, label='Actual Solar Generation')
    
    # Add annotation for the 2025 point
    plt.annotate('2025 (projected)', xy=(2025, 2718), xytext=(2023, 2800),
                fontsize=10, ha='center')
    
    # Draw projection lines for each WEO year
    for _, row in cur_data.iterrows():
        weo_year = row['Year']
        projections = []
        
        # Collect all projection years and values (including 2040)
        for year_col in ['2020', '2025', '2030', '2035', '2040']:  # Added back 2040
            if pd.notna(row[year_col]):
                try:
                    value = float(row[year_col])
                    projections.append((int(year_col), value))
                except (ValueError, TypeError):
                    continue
        
        if len(projections) > 0:
            print(f"Drawing {weo_year} WEO projections: {projections}")
            
            # Find the actual observation year to start the line from
            actual_year = None
            for _, actual_row in actual_data.iterrows():
                if actual_row['Year'] == weo_year:
                    actual_year = weo_year
                    break
            
            if actual_year is not None:
                # Draw line from actual observation to first projection
                if len(projections) > 0:
                    first_proj_year, first_proj_value = projections[0]
                    plt.plot([actual_year, first_proj_year], [actual_data[actual_data['Year'] == actual_year]['Actually got'].iloc[0], first_proj_value], 
                            color='gold', linewidth=2, alpha=0.8)
                    
                    # Draw lines between subsequent projections
                    for i in range(len(projections) - 1):
                        year1, value1 = projections[i]
                        year2, value2 = projections[i + 1]
                        plt.plot([year1, year2], [value1, value2], 
                                color='gold', linewidth=2, alpha=0.8)
                    
                    # Add markers for projection points
                    for year, value in projections:
                        plt.scatter(year, value, color='gold', s=50, alpha=0.8, edgecolors='black', linewidth=1)

    # Customize the plot
    plt.title('World Solar PV Generation vs. International Energy Agency’s Annual Predictions', fontsize=18, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Solar Generation (TWh)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper left')
    
    # Set x-axis limits to ensure all predictions are visible
    plt.xlim(2009, 2035)  # Start at 2009, cut off at 2035
    
    # Get all years for x-axis (including 2040 but keeping x-axis range limited)
    all_years = sorted(list(set(list(actual_data['Year']) + [2020, 2025, 2030, 2035])))  # Removed 2040 from ticks
    plt.xticks(all_years)
    
    # Set y-axis limits for log scale - start at 10 TWh for better visibility
    plt.ylim(bottom=10, top=10000)
    
    # Set y-axis to logarithmic scale (base 10)
    plt.yscale('log')
    
    # Improve grid for log scale
    plt.grid(True, alpha=0.3, which='major')
    plt.minorticks_on()
    plt.grid(True, alpha=0.1, which='minor')
    
    # Customize x-axis labels to use abbreviated years
    x_ticks = plt.xticks()[0]
    x_labels = []
    for year in x_ticks:
        if year >= 2030:
            x_labels.append(str(int(year)))  # Full year for 2030+
        else:
            x_labels.append(str(int(year))[-2:])  # Abbreviated for years < 2030
    plt.xticks(x_ticks, x_labels)
    
    # Set y-axis to show every second year to reduce crowding
    y_ticks = plt.yticks()[0]  # Get current y-ticks
    plt.yticks(y_ticks[::2])  # Show every second tick
    
    # Add attribution below the x-axis
    plt.figtext(0.98, 0.02, 'by @iamredave', ha='right', va='bottom', fontsize=10, style='italic')
    
    print(f"X-axis range: {plt.xlim()}")
    print(f"X-axis ticks: {plt.xticks()}")
    
    # Adjust layout to accommodate legend
    plt.tight_layout()
    
    # Create graphs directory if it doesn't exist
    Path("graphs").mkdir(exist_ok=True)
    
    # Save the plot
    plt.savefig("graphs/solar_generation_with_projections.png", dpi=300, bbox_inches='tight')
    print("Plot saved: graphs/solar_generation_with_projections.png")
    
    # Show the plot
    plt.show()


if __name__ == "__main__":
    plot_actual_solar_with_projections()
