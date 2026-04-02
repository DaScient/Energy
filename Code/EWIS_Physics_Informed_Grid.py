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


# EWIS: Energy, Weather, and Interoperability Suite
## Physics-Informed Grid Modeling & Battlespace Anomaly Injection

**Mission Scope:** Modern grid optimization requires more than statistical forecasting; it requires models that understand thermodynamics and electrical engineering. This notebook demonstrates a **Physics-Informed Neural Network (PINN)** approach to load management, evaluating an AI agent's ability to reroute power dynamically during a simulated DDIL event (e.g., extreme weather or cyber-attack on grid infrastructure).

**Key Capabilities:**
* **PINN Loss Functions:** Penalizes AI agents for violating Kirchhoff's Laws and thermal limits.
* **Battlespace Injection:** Simulates sudden capacity drops.
* **Interactive Analytics:** Plotly-driven interactive infrastructure dashboards.

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import torch
import torch.nn as nn

# --- 1. SYNTHETIC BATTLESPACE TELEMETRY ---
def generate_battlespace_grid(hours=48, anomaly_start=24, anomaly_duration=6):
    """Generates baseline grid data and injects a critical DDIL anomaly."""
    time = np.arange(hours)
    base_load = 500 + 200 * np.sin(np.pi * (time - 6) / 12) + np.random.normal(0, 10, hours)
    capacity = np.full(hours, 900.0)
    
    # Inject Battlespace Anomaly (e.g., EMP, Cyber-Attack, Extreme Heatwave)
    capacity[anomaly_start:anomaly_start+anomaly_duration] *= 0.60 # 40% capacity loss
    
    return pd.DataFrame({'Hour': time, 'Base_Load_MW': base_load, 'Line_Capacity_MW': capacity})

grid_df = generate_battlespace_grid()

# --- 2. PHYSICS-INFORMED AI AGENT (Mock PINN Architecture) ---
class EnergyAgentPINN(nn.Module):
    """A neural network constrained by physical grid laws."""
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 1))
        
    def forward(self, t, capacity):
        return self.net(torch.cat([t, capacity], dim=1))

def evaluate_pinn_agent(df):
    """Evaluates the agent's proposed DC load against physical constraints."""
    print("Evaluating PINN Agent under DDIL conditions...")
    # Simulated Agent Output (Agent learns to drop load during the anomaly)
    agent_dc_load = np.full(len(df), 250.0)
    anomaly_mask = df['Line_Capacity_MW'] < 800
    agent_dc_load[anomaly_mask] = 50.0 # Agent intelligently throttles compute
    
    df['Agent_Proposed_DC_Load'] = agent_dc_load
    df['Total_System_Load'] = df['Base_Load_MW'] + df['Agent_Proposed_DC_Load']
    df['Physics_Violation'] = df['Total_System_Load'] > df['Line_Capacity_MW']
    return df

results_df = evaluate_pinn_agent(grid_df)

# --- 3. INTERACTIVE BATTLESPACE VISUALIZATION ---
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    subplot_titles=("Grid Load vs. Dynamic Capacity", "Agent Performance & Physics Violations"))

# Top Plot: Load & Capacity
fig.add_trace(go.Scatter(x=results_df['Hour'], y=results_df['Line_Capacity_MW'], 
                         line=dict(color='red', width=3, dash='dash'), name='Thermal Capacity Limit'), row=1, col=1)
fig.add_trace(go.Scatter(x=results_df['Hour'], y=results_df['Base_Load_MW'], 
                         fill='tozeroy', line=dict(color='gray'), name='Civilian Base Load'), row=1, col=1)
fig.add_trace(go.Bar(x=results_df['Hour'], y=results_df['Agent_Proposed_DC_Load'], 
                     base=results_df['Base_Load_MW'], marker_color='cyan', name='AI Datacenter Load'), row=1, col=1)

# Bottom Plot: Violations
violations = results_df[results_df['Physics_Violation']]
fig.add_trace(go.Scatter(x=results_df['Hour'], y=results_df['Total_System_Load'], 
                         line=dict(color='orange', width=2), name='Total Load'), row=2, col=1)
fig.add_trace(go.Scatter(x=violations['Hour'], y=violations['Total_System_Load'], 
                         mode='markers', marker=dict(color='red', size=12, symbol='x'), name='Critical Overload'), row=2, col=1)

fig.update_layout(height=700, template='plotly_dark', title_text="EWIS: Battlespace Grid Optimization & Agent Evaluation")
fig.show()
