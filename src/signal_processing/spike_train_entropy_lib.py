import numpy as np
from scipy.stats import entropy

class NeuralInformationTheory:
    """
    Translates electrophysiology from descriptive neurobiology into 
    quantitative communication science by measuring information entropy.
    """
    @staticmethod
    def shannon_entropy(spike_train_bins: np.ndarray) -> float:
        """
        Calculates H(X) = -Σ p(x) log p(x) for a binned spike train.
        Quantifies the uncertainty (or richness) of the neural state.
        """
        # Calculate probabilities of different firing rates/states in the bins
        _, counts = np.unique(spike_train_bins, return_counts=True)
        probabilities = counts / len(spike_train_bins)
        return entropy(probabilities, base=2)

    @staticmethod
    def mutual_information(stimulus_bins: np.ndarray, response_bins: np.ndarray) -> float:
        """
        Calculates I(X;Y) = H(X) + H(Y) - H(X,Y).
        Measures how much uncertainty about the stimulus is reduced by observing the spike train.
        """
        h_x = NeuralInformationTheory.shannon_entropy(stimulus_bins)
        h_y = NeuralInformationTheory.shannon_entropy(response_bins)
        
        # Calculate joint entropy H(X,Y)
        joint_states = list(zip(stimulus_bins, response_bins))
        _, counts = np.unique(joint_states, axis=0, return_counts=True)
        joint_probs = counts / len(joint_states)
        h_xy = entropy(joint_probs, base=2)
        
        return h_x + h_y - h_xy
