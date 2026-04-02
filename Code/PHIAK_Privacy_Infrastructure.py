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
