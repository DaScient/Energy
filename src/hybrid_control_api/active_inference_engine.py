import numpy as np

class ActiveInferenceEngine:
    """
    Implements a Predictive Processing loop. Rather than passively receiving 
    sensory data, the biological system continually estimates the causes of its inputs.
    """
    def __init__(self, complexity_weight: float = 0.1):
        self.priors = np.zeros(10) # Internal model predictions
        self.complexity_weight = complexity_weight

    def step(self, sensory_evidence: np.ndarray) -> np.ndarray:
        """
        Executes one loop of perception-action updating.
        """
        # 1. Calculate Prediction Error (Surprise)
        prediction_error = sensory_evidence - self.priors
        
        # 2. Calculate Variational Free Energy (F ≈ Error + Complexity)
        complexity_cost = self.complexity_weight * np.sum(np.abs(self.priors))
        free_energy = np.sum(prediction_error**2) + complexity_cost
        
        # 3. Update internal model to minimize future error (Learning)
        learning_rate = 0.05
        self.priors += learning_rate * prediction_error
        
        # 4. Generate Action Policy to change the world state
        action_command = -learning_rate * prediction_error
        
        return action_command, free_energy

# Example integration step
engine = ActiveInferenceEngine()
sensory_input = np.random.uniform(0, 1, 10)
action, current_fe = engine.step(sensory_input)
print(f"Action Policy Dispatched. Current System Free Energy: {current_fe:.3f}")
