class NeuromorphicMiddleware:
    """
    The translation layer. Converts continuous, clock-based digital workloads 
    into sparse, event-driven spiking formats digestible by organoid biology.
    """
    def __init__(self, encoding_scheme: str = "rate_coding"):
        self.encoding = encoding_scheme

    def digital_to_spikes(self, digital_vector: list, duration_ms: int) -> list:
        """
        Converts a digital array (e.g., pixel intensities or continuous control signals)
        into a train of stimulation pulses.
        """
        spike_trains = []
        for value in digital_vector:
            if self.encoding == "rate_coding":
                # Higher value = higher frequency of spikes
                freq_hz = value * 100 
                num_spikes = int((freq_hz * duration_ms) / 1000)
                train = [1] * num_spikes + [0] * (duration_ms - num_spikes)
                spike_trains.append(train)
            # Future expansion for temporal coding, phase coding, etc.
        return spike_trains

    def spikes_to_digital(self, decoded_state: list) -> list:
        """Translates biological readout back to standard digital floats for the OS."""
        return [float(state) for state in decoded_state]
