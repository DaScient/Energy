/// Manages the artificial temporal geometry between distributed living modules.
pub struct DelayLineManager {
    conduction_velocity_m_s: f64, // 'v'
}

impl DelayLineManager {
    pub fn new(estimated_velocity: f64) -> Self {
        DelayLineManager {
            conduction_velocity_m_s: estimated_velocity,
        }
    }

    /// Calculates expected delay τ = L / v
    pub fn calculate_delay_ms(&self, path_length_mm: f64) -> f64 {
        let length_m = path_length_mm / 1000.0;
        let delay_s = length_m / self.conduction_velocity_m_s;
        delay_s * 1000.0 // Convert to milliseconds
    }

    /// Buffers a digital spike event before routing it to the destination organoid
    pub fn enforce_delay(&self, event_timestamp: u64, path_length_mm: f64) -> u64 {
        let required_delay_ms = self.calculate_delay_ms(path_length_mm);
        // Returns the target execution timestamp for the stimulation pulse
        event_timestamp + (required_delay_ms as u64)
    }
}
