# WOIK: Water Ops Interoperability Kit
## Water-Energy Nexus & HPC Thermal Management

#This notebook simulates the thermal transfer network of a high-performance compute (HPC) cluster. By modeling the system as a directed graph representing fluid dynamics and heat exchange, we can evaluate an AI agent's ability to optimize coolant flow, reducing Water Usage Effectiveness (WUE) during peak compute loads.

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# 1. Initialize the Hydraulic/Thermal Graph
def build_cooling_network():
    """Builds a directed graph representing server racks and coolant pipes."""
    G = nx.DiGraph()
    # Nodes: representing server racks with current thermal load (kW)
    racks = ['Rack_A', 'Rack_B', 'Rack_C', 'Rack_D']
    thermal_loads = [15, 45, 10, 50] # kW of heat generated
    
    for i, rack in enumerate(racks):
        G.add_node(rack, type='server', heat_kw=thermal_loads[i])
        
    # Chiller plant
    G.add_node('Chiller', type='cooling', max_capacity_kw=150)
    
    # Edges: representing coolant flow paths
    edges = [('Chiller', 'Rack_A'), ('Chiller', 'Rack_B'), 
             ('Rack_A', 'Rack_C'), ('Rack_B', 'Rack_D'),
             ('Rack_C', 'Chiller'), ('Rack_D', 'Chiller')]
    G.add_edges_from(edges)
    return G

cooling_net = build_cooling_network()

# 2. Fluid Dynamic Evaluation Engine
def evaluate_agent_flow_allocation(G, agent_flow_commands):
    """
    Evaluates if the AI agent's proposed water flow (Liters/Sec) 
    is sufficient to extract the heat without violating physics.
    Specific Heat of Water = 4.18 kJ/(kg*C)
    """
    print("--- WOIK Thermal-Hydraulic Evaluation ---")
    specific_heat_water = 4.18 
    max_temp_delta = 10 # Max allowable water temp increase (Celsius)
    
    physics_violations = 0
    total_water_used = sum(agent_flow_commands.values())
    
    for node, data in G.nodes(data=True):
        if data['type'] == 'server':
            heat = data['heat_kw']
            flow_lps = agent_flow_commands.get(node, 0)
            
            # Physics: Q = m * c * dT -> dT = Q / (m * c)
            if flow_lps == 0:
                print(f"[VIOLATION] {node}: Zero flow! Thermal runaway imminent.")
                physics_violations += 1
                continue
                
            temp_increase = heat / (flow_lps * specific_heat_water)
            
            if temp_increase > max_temp_delta:
                print(f"[VIOLATION] {node}: Temp delta {temp_increase:.1f}C exceeds safe limit ({max_temp_delta}C). Need more flow.")
                physics_violations += 1
            else:
                print(f"[SAFE] {node}: Heat {heat}kW extracted safely with {flow_lps} L/s.")
                
    print(f"\nTotal System Water Flow: {total_water_used} L/s")
    print(f"Total Physics Violations: {physics_violations}")
    return physics_violations == 0

# 3. Simulate AI Agent Action
# Agent proposes this flow based on ML predictions (intentionally under-cooling Rack_D to test engine)
ai_proposed_flow = {
    'Rack_A': 0.5,
    'Rack_B': 1.2,
    'Rack_C': 0.3,
    'Rack_D': 0.8  # Too low for 50kW!
}

# Run Evaluation
success = evaluate_agent_flow_allocation(cooling_net, ai_proposed_flow)

# Visualize Network
pos = nx.spring_layout(cooling_net)
colors = ['cyan' if cooling_net.nodes[n]['type'] == 'cooling' else 'red' for n in cooling_net.nodes]
nx.draw(cooling_net, pos, with_labels=True, node_color=colors, node_size=2000, font_weight='bold', arrows=True)
plt.title("Data Center Hydraulic/Thermal Network")
plt.show()
