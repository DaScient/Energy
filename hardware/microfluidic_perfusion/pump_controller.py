import time
import logging
from typing import Dict

class PerfusionController:
    """
    Manages active microfluidic perfusion to prevent diffusion-limited necrotic cores.
    Integrates flow control, nutrient delivery, and waste removal.
    """
    def __init__(self, port: str, target_flow_rate_ul_min: float = 2.5):
        self.port = port
        self.target_flow_rate = target_flow_rate_ul_min
        self.current_flow_rate = 0.0
        self.is_running = False
        logging.info(f"Initialized Microfluidic Perfusion on {self.port}")

    def read_sensor_telemetry(self) -> Dict[str, float]:
        """Reads downstream sensors to adapt flow dynamically."""
        # Mocking sensor reads for oxygen tension and lactate (waste) build-up
        return {"o2_tension_mmhg": 140.5, "lactate_mm": 1.2, "ph": 7.35}

    def regulate_flow(self):
        """Adjusts pump speed to maintain homeostasis in the diffusion-limited core."""
        self.is_running = True
        while self.is_running:
            telemetry = self.read_sensor_telemetry()
            
            # Increase flow if oxygen drops or waste accumulates
            if telemetry["o2_tension_mmhg"] < 130.0 or telemetry["lactate_mm"] > 2.0:
                self.current_flow_rate = min(self.target_flow_rate * 1.5, 5.0)
                logging.warning("Metabolic stress detected. Increasing perfusion rate.")
            else:
                self.current_flow_rate = self.target_flow_rate
                
            self._send_pump_command(self.current_flow_rate)
            time.sleep(10) # 10-second control loop

    def _send_pump_command(self, rate: float):
        # Hardware specific I2C or Serial command to the physical pump
        pass
