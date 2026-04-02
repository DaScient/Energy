import yaml

class OpsinCalibrator:
    """
    Translates digital stimulation requests into specific optical power 
    outputs based on the expressed channelrhodopsin properties.
    """
    def __init__(self, opsin_profile: str):
        # E.g., ChR2 (Blue, excitatory), NpHR (Yellow, inhibitory), Chrimson (Red, excitatory)
        self.opsins = {
            "ChR2": {"wavelength_nm": 470, "threshold_mw_mm2": 1.0, "kinetics_ms": 10},
            "ChrimsonR": {"wavelength_nm": 590, "threshold_mw_mm2": 2.5, "kinetics_ms": 15},
            "NpHR": {"wavelength_nm": 589, "threshold_mw_mm2": 5.0, "kinetics_ms": 20}
        }
        self.active_opsin = self.opsins.get(opsin_profile)

    def calculate_optical_power(self, depth_um: float, required_depolarization: float) -> float:
        """
        Calculates required LED power accounting for tissue scattering.
        Light intensity drops exponentially through dense neural tissue.
        """
        scattering_coeff = 0.01 # Approximate scattering in brain tissue
        base_power = self.active_opsin["threshold_mw_mm2"] * required_depolarization
        
        # Beer-Lambert approximation for required surface power
        surface_power = base_power * (2.718 ** (scattering_coeff * (depth_um / 100)))
        return round(surface_power, 2)

# Example Usage
calibrator = OpsinCalibrator("ChrimsonR")
required_power = calibrator.calculate_optical_power(depth_um=500, required_depolarization=1.5)
print(f"Set 590nm LED to {required_power} mW/mm^2 to stimulate target depth.")
