use std::collections::HashMap;

/// Represents a distinct extracellular spike waveform template
struct SpikeTemplate {
    id: u32,
    waveform: Vec<f64>,
    variance_tolerance: f64,
}

pub struct RealTimeSpikeSorter {
    templates: HashMap<u32, SpikeTemplate>,
    sampling_rate_hz: u32,
}

impl RealTimeSpikeSorter {
    pub fn new(sampling_rate: u32) -> Self {
        RealTimeSpikeSorter {
            templates: HashMap::new(),
            sampling_rate_hz: sampling_rate,
        }
    }

    /// Fast template matching using Sum of Squared Differences (SSD)
    pub fn detect_events(&self, raw_stream: &[f64]) -> Vec<(usize, u32)> {
        let mut detected_events = Vec::new();
        let window_size = 30; // approx 1ms at 30kHz

        for i in 0..(raw_stream.len() - window_size) {
            let window = &raw_stream[i..i + window_size];

            for template in self.templates.values() {
                let ssd: f64 = window.iter().zip(template.waveform.iter())
                                     .map(|(s, t)| (s - t).powi(2))
                                     .sum();

                if ssd < template.variance_tolerance {
                    // Event detected
                    detected_events.push((i, template.id));
                }
            }
        }
        detected_events
    }
}
