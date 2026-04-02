# EWIS: Energy, Weather, and Interoperability Suite

## Physics-Informed Grid Modeling & Load Optimization



This notebook demonstrates the EWIS engine's ability to enforce physical grid constraints. It acts as the physics boundary for AI agents, ensuring that proposed load optimizations (e.g., for HPC data centers) do not violate thermal line limits or exceed localized carbon-intensity thresholds.



import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

from scipy.optimize import minimize



# 1. Synthetic Grid Telemetry Generator

def generate_grid_state(hours=24):

    """Generates synthetic baseline load, capacity, and carbon intensity."""

    time = np.arange(hours)

    base_load = 500 + 200 * np.sin(np.pi * (time - 6) / 12) # MW

    line_capacity = np.full(hours, 800) # MW thermal limit

    carbon_intensity = 300 + 150 * np.cos(np.pi * (time - 12) / 12) # gCO2/kWh

    

    return pd.DataFrame({

        'Hour': time,

        'Base_Load_MW': base_load,

        'Capacity_MW': line_capacity,

        'Carbon_gCO2_kWh': carbon_intensity

    })



grid_data = generate_grid_state()



# 2. Physics & Carbon Constrained Optimizer

def optimize_dc_load(grid_df, target_dc_load_mwh=240):

    """

    Distributes Data Center (DC) load to minimize carbon footprint 

    WITHOUT violating physical line capacities.

    """

    def objective(dc_load_profile):

        # Minimize total carbon emissions from the DC load

        return np.sum(dc_load_profile * grid_df['Carbon_gCO2_kWh'])



    def constraint_capacity(dc_load_profile):

        # Physical constraint: Base Load + DC Load must be <= Line Capacity

        return grid_df['Capacity_MW'] - (grid_df['Base_Load_MW'] + dc_load_profile)



    def constraint_total_work(dc_load_profile):

        # Operational constraint: DC must complete its total daily workload

        return np.sum(dc_load_profile) - target_dc_load_mwh



    # Initial guess: flat load distribution

    x0 = np.full(24, target_dc_load_mwh / 24)

    

    # Bounds: DC load cannot be negative, max 50MW per hour

    bounds = [(0, 50) for _ in range(24)]

    

    constraints = [

        {'type': 'ineq', 'fun': constraint_capacity}, # Must be >= 0

        {'type': 'eq', 'fun': constraint_total_work}  # Must == 0

    ]



    result = minimize(objective, x0, bounds=bounds, constraints=constraints)

    return result.x



# 3. Execution & Visualization

optimized_dc_load = optimize_dc_load(grid_data)

grid_data['Optimized_DC_Load'] = optimized_dc_load

grid_data['Total_System_Load'] = grid_data['Base_Load_MW'] + optimized_dc_load



plt.figure(figsize=(12, 5))

plt.plot(grid_data['Hour'], grid_data['Capacity_MW'], 'r--', label='Thermal Line Limit')

plt.fill_between(grid_data['Hour'], 0, grid_data['Base_Load_MW'], color='lightgray', label='Base Load')

plt.bar(grid_data['Hour'], grid_data['Optimized_DC_Load'], bottom=grid_data['Base_Load_MW'], 

        color='green', alpha=0.7, label='Smart AI DC Load')

plt.twinx()

plt.plot(grid_data['Hour'], grid_data['Carbon_gCO2_kWh'], 'k:', label='Carbon Intensity (Right Axis)')

plt.title("EWIS: Physics-Constrained AI Load Shifting")

plt.xlabel("Hour of Day")

plt.legend(loc='upper left')

plt.show()
