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



# WOIK: Water Ops Interoperability Kit
## GNN-Ready Fluid Dynamics & Dynamic Workload Cooling

**Mission Scope:** High-Performance Computing (HPC) facilities running frontier AI models generate massive, volatile thermal loads. This notebook leverages graph theory—a precursor to Graph Neural Networks (GNNs)—to map the thermodynamic energy-water nexus. We evaluate whether an AI facility agent can preemptively route coolant flow *before* a massive LLM training run initiates thermal runaway.

**Key Capabilities:**
* **Graph-Based Telemetry:** Maps physical infrastructure (chillers, pumps, racks) as spatial nodes.
* **Predictive Thermal Spikes:** Simulates massive GPU utilization events.
* **Fluid Mechanics Constraints:** Enforces specific heat capacity and flow rate limits.


import networkx as nx
import plotly.graph_objects as go
import numpy as np

# --- 1. SPATIAL INFRASTRUCTURE GRAPH ---
def build_hpc_fluid_graph():
    """Constructs the cooling topology for a classified HPC cluster."""
    G = nx.DiGraph()
    # Nodes: X, Y coords for plotting, plus base thermodynamic properties
    G.add_node('Main_Chiller', pos=(0, 2), type='source', temp_c=10, max_flow_lps=500)
    G.add_node('Pump_Station_Alpha', pos=(1, 2), type='pump', status='ONLINE')
    G.add_node('GPU_Cluster_1', pos=(2, 3), type='compute', load_kw=50)  # Idle
    G.add_node('GPU_Cluster_2', pos=(2, 1), type='compute', load_kw=850) # LLM Training Run!
    G.add_node('Heat_Exchanger', pos=(3, 2), type='return', temp_limit_c=45)
    
    # Fluid pathways
    G.add_edges_from([('Main_Chiller', 'Pump_Station_Alpha'), 
                      ('Pump_Station_Alpha', 'GPU_Cluster_1'),
                      ('Pump_Station_Alpha', 'GPU_Cluster_2'),
                      ('GPU_Cluster_1', 'Heat_Exchanger'),
                      ('GPU_Cluster_2', 'Heat_Exchanger')])
    return G

hpc_graph = build_hpc_fluid_graph()

# --- 2. THERMODYNAMIC EVALUATION ENGINE ---
def evaluate_fluid_routing(G, agent_flow_commands):
    """Calculates specific heat transfer. Q = m * c * dT"""
    specific_heat_h2o = 4.186 # kJ/(kg*C)
    node_x, node_y, node_colors, hover_text = [], [], [], []
    
    for node, attrs in G.nodes(data=True):
        pos = attrs['pos']
        node_x.append(pos[0])
        node_y.append(pos[1])
        
        if attrs['type'] == 'compute':
            flow = agent_flow_commands.get(node, 0.1)
            delta_t = attrs['load_kw'] / (flow * specific_heat_h2o)
            out_temp = 10 + delta_t # Base coolant temp is 10C
            
            if out_temp > 45.0:
                node_colors.append('red') # Thermal Runaway
                hover_text.append(f"{node}<br>Load: {attrs['load_kw']}kW<br>Flow: {flow} L/s<br>Temp Out: {out_temp:.1f}C (CRITICAL)")
            else:
                node_colors.append('cyan') # Safe
                hover_text.append(f"{node}<br>Load: {attrs['load_kw']}kW<br>Flow: {flow} L/s<br>Temp Out: {out_temp:.1f}C (SAFE)")
        else:
            node_colors.append('gray')
            hover_text.append(f"{node} ({attrs['type']})")

    return node_x, node_y, node_colors, hover_text

# Simulated Agent Failure (Underestimates LLM Training load)
ai_proposed_flow = {'GPU_Cluster_1': 50, 'GPU_Cluster_2': 100} # 100 L/s is too low for 850kW!
n_x, n_y, n_cols, n_text = evaluate_fluid_routing(hpc_graph, ai_proposed_flow)

# --- 3. INTERACTIVE TOPOLOGY VISUALIZATION ---
edge_x, edge_y = [], []
for edge in hpc_graph.edges():
    x0, y0 = hpc_graph.nodes[edge[0]]['pos']
    x1, y1 = hpc_graph.nodes[edge[1]]['pos']
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

fig = go.Figure()
fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=2, color='#888'), hoverinfo='none'))
fig.add_trace(go.Scatter(x=n_x, y=n_y, mode='markers', hoverinfo='text', text=n_text,
                         marker=dict(size=40, color=n_cols, line=dict(width=2, color='white'))))

fig.update_layout(title="WOIK: HPC Thermal-Hydraulic Network Evaluation", 
                  template='plotly_dark', showlegend=False, xaxis=dict(visible=False), yaxis=dict(visible=False))
fig.show()
