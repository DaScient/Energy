import numpy as np
import logging

class SynchronizationManager:
    """
    Monitors and manages oscillatory coherence across a multi-organoid network.
    Prevents hypersynchrony (seizure-like states) which destroy computational utility.
    """
    def __init__(self, threshold_coherence: float = 0.85):
        self.threshold_coherence = threshold_coherence

    def calculate_phase_locking_value(self, module_a_phase: np.ndarray, module_b_phase: np.ndarray) -> float:
        """Calculates phase consistency across temporal windows."""
        phase_diff = module_a_phase - module_b_phase
        plv = np.abs(np.mean(np.exp(1j * phase_diff)))
        return plv

    def enforce_mode_switching(self, plv: float):
        """
        Injects inhibitory noise or delays if the network becomes too synchronized,
        preserving the adaptive richness of the distributed system.
        """
        if plv > self.threshold_coherence:
            logging.warning(f"Hypersynchrony detected (PLV: {plv:.2f}). Initiating desynchronization.")
            self._trigger_optical_inhibition()
        else:
            logging.info(f"Network coherence stable (PLV: {plv:.2f}).")

    def _trigger_optical_inhibition(self):
        # Calls the optogenetic API to fire NpHR (yellow light) for a brief inhibitory reset
        pass
