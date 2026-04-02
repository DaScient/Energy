class OrbitalMaturationController:
    """
    Manages the mechanical agitation required to enhance nutrient diffusion 
    and support the 3D structural maturation of cortical organoids.
    """
    def __init__(self, shaker_port: str):
        self.shaker_port = shaker_port
        self.current_rpm = 0

    def calculate_optimal_rpm(self, organoid_diameter_mm: float, day_of_culture: int) -> int:
        """
        Dynamically adjusts orbital RPM. Larger tissues require higher RPM 
        to break the diffusion boundary layer, but excessive shear stress causes damage.
        """
        base_rpm = 60
        # Increase RPM slightly as tissue volume grows
        size_factor = min(organoid_diameter_mm * 5, 30) 
        
        # Glial support phase (Days 50+) requires gentler shear
        developmental_modifier = -10 if day_of_culture > 50 else 0
        
        target_rpm = int(base_rpm + size_factor + developmental_modifier)
        return min(max(target_rpm, 40), 95) # Clamp between 40 and 95 RPM

    def apply_agitation(self, rpm: int):
        self.current_rpm = rpm
        # I2C/Serial command to the physical orbital shaker incubator
        print(f"Orbital Shaker set to {self.current_rpm} RPM to optimize 3D growth.")
