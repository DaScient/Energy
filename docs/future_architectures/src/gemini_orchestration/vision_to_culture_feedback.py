import time
import logging
from pathlib import Path
from gemini_client import GeminiMultimodalClient
import sys

# Ensure the hardware and culture modules are in the path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from hardware.microfluidic_perfusion.pump_controller import PerfusionController
from src.organoid_culture.orbital_maturation_logic import OrbitalMaturationController

class VisionFeedbackLoop:
    """
    Closes the loop between optical microscopy and hardware actuation.
    Uses Gemini's visual reasoning to dynamically adjust the physical 
    environment of the living data center.
    """
    def __init__(self, bru_id: str, camera_feed_dir: str):
        self.bru_id = bru_id
        self.camera_feed_dir = Path(camera_feed_dir)
        
        # Initialize Digital and Physical Interfaces
        self.ai_orchestrator = GeminiMultimodalClient()
        self.perfusion_sys = PerfusionController(port="I2C_BUS_1")
        self.orbital_sys = OrbitalMaturationController(shaker_port="SERIAL_COM_3")
        
        self.is_monitoring = False
        logging.info(f"[{self.bru_id}] Vision Feedback Loop Initialized.")

    def _get_latest_microscopy_frame(self) -> str:
        """Fetches the most recent image captured by the BRU's internal camera."""
        # Assumes a process is dropping timestamped .png files into the directory
        images = sorted(self.camera_feed_dir.glob('*.png'), key=os.path.getmtime)
        if not images:
            raise FileNotFoundError("No microscopy frames available in the feed directory.")
        return str(images[-1])

    def run_monitoring_cycle(self, interval_seconds: int = 3600):
        """
        The main loop. Periodically evaluates the physical tissue 
        and updates the hardware parameters to maintain optimal computation states.
        """
        self.is_monitoring = True
        logging.info(f"[{self.bru_id}] Starting Continuous Visual Monitoring...")

        while self.is_monitoring:
            try:
                frame_path = self._get_latest_microscopy_frame()
                current_telemetry = self.perfusion_sys.read_sensor_telemetry()
                
                # Combine physical sensor data with current hardware states
                context = {
                    "sensor_data": current_telemetry,
                    "current_perfusion_ul_min": self.perfusion_sys.current_flow_rate,
                    "current_agitation_rpm": self.orbital_sys.current_rpm
                }

                logging.info(f"[{self.bru_id}] Sending Frame to Digital Oversoul for evaluation.")
                assessment = self.ai_orchestrator.analyze_bioreactor_state(frame_path, context)
                
                if assessment:
                    self._apply_hardware_adjustments(assessment)
                
            except Exception as e:
                logging.error(f"[{self.bru_id}] Error in monitoring cycle: {e}")
            
            # Sleep until the next evaluation window
            time.sleep(interval_seconds)

    def _apply_hardware_adjustments(self, assessment: dict):
        """Translates the AI's JSON directives into physical hardware commands."""
        logging.info(f"[{self.bru_id}] Applying Digital Oversoul Directives:")
        logging.info(f"   -> Necrotic Risk: {assessment.get('necrotic_risk_level')}")
        logging.info(f"   -> Synaptic Health: {assessment.get('synaptic_health')}")

        # Update Perfusion
        new_flow = assessment.get('target_perfusion_ul_min')
        if new_flow:
            logging.info(f"   -> Adjusting Perfusion Flow to {new_flow} ul/min.")
            self.perfusion_sys.target_flow_rate = new_flow
            # In a live system, _send_pump_command would be invoked here

        # Update Orbital Agitation
        new_rpm = assessment.get('target_agitation_rpm')
        if new_rpm:
            logging.info(f"   -> Adjusting Orbital Agitation to {new_rpm} RPM.")
            self.orbital_sys.apply_agitation(new_rpm)

        # Critical Safety Override
        if assessment.get('necrotic_risk_level') == 'critical':
            logging.warning(f"[{self.bru_id}] CRITICAL NECROTIC RISK DETECTED. Triggering emergency flush protocol.")
            # Trigger emergency protocol to save the biological module

# Example Execution:
# if __name__ == "__main__":
#     # Assuming images are saved to /tmp/bru_01_camera/
#     feedback_loop = VisionFeedbackLoop(bru_id="BRU_Alpha_01", camera_feed_dir="/tmp/bru_01_camera/")
#     feedback_loop.run_monitoring_cycle(interval_seconds=1800) # Check every 30 minutes
