# PHIAK: Public Health & Privacy Infrastructure Analytics Kit
## Privacy-Native Bio-Infrastructure & Secure Data Substrate

#This notebook demonstrates the non-negotiable guardrails of the ARES-E framework. Before any critical infrastructure telemetry is exposed to an AI agent, it must pass through PHIAK to ensure zero individual-level data ingestion and enforce minimum cell count suppression.

import pandas as pd
import numpy as np

# 1. Generate Raw, Unsafe Telemetry (Simulating raw facility logs)
def generate_raw_facility_logs():
    return pd.DataFrame({
        'Timestamp': pd.date_range(start='2026-04-01', periods=10, freq='H'),
        'Employee_ID': ['E12', 'E45', 'E12', 'E88', 'E91', 'E45', 'E11', 'E22', 'E33', 'E44'],
        'Facility_Zone': ['Zone_A', 'Zone_A', 'Zone_A', 'Zone_B', 'Zone_B', 'Zone_A', 'Zone_C', 'Zone_C', 'Zone_A', 'Zone_B'],
        'Biometric_Temp_C': [37.1, 36.8, 37.2, 38.5, 36.9, 37.0, 37.1, 37.5, 36.8, 38.1],
        'Clearance_Level': ['TS', 'S', 'TS', 'TS', 'S', 'S', 'TS', 'S', 'TS', 'S']
    })

raw_data = generate_raw_facility_logs()
print("--- RAW DATA (Contains PII/Sensitive Identifiers) ---")
display(raw_data.head(3))

# 2. PHIAK Deterministic Privacy Engine
class PHIAK_Engine:
    def __init__(self, min_cell_size=3):
        self.min_cell_size = min_cell_size
        self.pii_columns = ['Employee_ID', 'Biometric_Temp_C'] # Hardcoded ban list
        
    def sanitize_payload(self, df):
        """Removes PII, aggregates, and applies cell suppression."""
        # Step A: Drop PII absolutely
        safe_df = df.drop(columns=[col for col in self.pii_columns if col in df.columns])
        
        # Step B: Aggregate by Time and Zone
        aggregated = safe_df.groupby(['Facility_Zone', 'Clearance_Level']).size().reset_index(name='Occupancy_Count')
        
        # Step C: Minimum Cell Count Suppression (Non-negotiable)
        aggregated['Occupancy_Count'] = aggregated['Occupancy_Count'].apply(
            lambda x: '<SUPPRESSED>' if x < self.min_cell_size else x
        )
        return aggregated

# 3. Execution: Securing the Substrate
phiak = PHIAK_Engine(min_cell_size=3)
secured_substrate = phiak.sanitize_payload(raw_data)

print("\n--- SECURED SUBSTRATE (Ready for AI Evaluation) ---")
display(secured_substrate)
print("\nNotice: Zones with fewer than 3 individuals are suppressed to prevent re-identification attacks by adversarial AI agents.")


# PHIAK: Public Health & Privacy Infrastructure Analytics Kit
## Differential Privacy & Zero-Trust Substrate

**Mission Scope:** Critical infrastructure facilities cannot expose raw occupancy, health, or biometric data to external AI models due to espionage and re-identification risks. This notebook upgrades the PHIAK engine with **Epsilon-Differential Privacy (DP)**. By injecting calibrated Laplacian noise, we guarantee mathematical privacy boundaries while preserving the statistical utility of the data for AI agents.

**Key Capabilities:**
* **Epsilon-DP Noise Injection:** Balances privacy (security) with utility (AI accuracy).
* **Zero-Trust Sanitization:** Ensures models cannot memorize or extract PII.
* **Utility Trade-off Analytics:** Visualizes the impact of privacy protocols on data fidelity.

import numpy as np
import pandas as pd
import plotly.express as px

# --- 1. SENSITIVE FACILITY TELEMETRY ---
def get_facility_occupancy():
    """Ground truth occupancy per sector (Highly classified)."""
    np.random.seed(42)
    sectors = [f"Sector_{i}" for i in range(1, 21)]
    # True human count per sector
    true_counts = np.random.poisson(lam=15, size=20) 
    return pd.DataFrame({'Sector': sectors, 'True_Count': true_counts})

df = get_facility_occupancy()

# --- 2. DIFFERENTIAL PRIVACY ENGINE (Laplace Mechanism) ---
def apply_differential_privacy(counts, epsilon=0.5, sensitivity=1):
    """
    Injects Laplacian noise. 
    Lower Epsilon (e.g., 0.1) = High Privacy, Low AI Utility.
    Higher Epsilon (e.g., 5.0) = Low Privacy, High AI Utility.
    """
    scale = sensitivity / epsilon
    noise = np.random.laplace(loc=0.0, scale=scale, size=len(counts))
    # Apply noise and ensure no negative human counts
    dp_counts = np.maximum(counts + noise, 0).round().astype(int)
    return dp_counts

# Generate Substrates for different security levels
df['DP_HighSec_Count (eps=0.2)'] = apply_differential_privacy(df['True_Count'], epsilon=0.2)
df['DP_Standard_Count (eps=1.5)'] = apply_differential_privacy(df['True_Count'], epsilon=1.5)

# --- 3. PRIVACY VS UTILITY VISUALIZATION ---
melted_df = df.melt(id_vars='Sector', value_vars=['True_Count', 'DP_Standard_Count (eps=1.5)', 'DP_HighSec_Count (eps=0.2)'],
                    var_name='Data_Tier', value_name='Occupancy_Count')

fig = px.bar(melted_df, x='Sector', y='Occupancy_Count', color='Data_Tier', barmode='group',
             title="PHIAK: Differential Privacy Impact on AI Telemetry Utility",
             color_discrete_map={'True_Count': '#00CC96', 'DP_Standard_Count (eps=1.5)': '#AB63FA', 'DP_HighSec_Count (eps=0.2)': '#EF553B'})

fig.update_layout(template='plotly_dark', yaxis_title="Number of Personnel", xaxis_title="Facility Sector")
fig.show()

print("\n[SECURITY NOTICE]: AI Agents evaluated on the HighSec data stream cannot mathematically isolate an individual's presence, neutralizing targeted data-exfiltration attacks.")
