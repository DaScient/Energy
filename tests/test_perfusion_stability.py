import unittest
from hardware.microfluidic_perfusion.pump_controller import PerfusionController

class TestPerfusionStability(unittest.TestCase):
    """
    Validates that the microfluidic life-support systems maintain strict
    metabolic homeostasis, preventing the formation of necrotic cores.
    """
    def setUp(self):
        self.controller = PerfusionController(port="VIRTUAL_COM_1", target_flow_rate_ul_min=2.5)

    def test_waste_removal_and_oxygenation(self):
        """
        Simulates telemetry to ensure the system correctly monitors oxygenation, 
        pH, and waste accumulation over time.
        """
        telemetry = self.controller.read_sensor_telemetry()
        
        # O2 tension must remain high enough to penetrate the tissue core
        self.assertTrue(telemetry["o2_tension_mmhg"] > 130.0, "FAIL: Hypoxia detected in tissue core.")
        
        # Acidosis indicates failing waste clearance
        self.assertTrue(7.35 <= telemetry["ph"] <= 7.45, "FAIL: pH out of physiological bounds.")
        
        # High lactate indicates anaerobic stress
        self.assertTrue(telemetry["lactate_mm"] < 2.0, "FAIL: Waste accumulation exceeds clearance rate.")

if __name__ == '__main__':
    unittest.main()
