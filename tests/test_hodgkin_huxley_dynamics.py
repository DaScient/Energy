import unittest
import numpy as np
from src.signal_processing.hodgkin_huxley_model import HodgkinHuxleyModel


class TestHodgkinHuxleyDynamics(unittest.TestCase):
    """
    Validates membrane voltage balance using the Hodgkin-Huxley conductance model:

        C_m * dV/dt = I_ext - g_Na*m^3*h*(V - E_Na)
                             - g_K*n^4*(V - E_K)
                             - g_L*(V - E_L)
    """

    def setUp(self):
        self.model = HodgkinHuxleyModel()

    def test_resting_potential_stability(self):
        """
        With zero external current the membrane should remain near resting potential.
        A healthy resting state is required before any stimulation protocol.
        """
        _, V = self.model.simulate(t_end=20.0, dt=0.01, I_ext=0.0)
        # Voltage must stay within physiological resting range
        self.assertTrue(
            np.all(V > -90.0) and np.all(V < -50.0),
            "FAIL: Resting potential outside expected physiological bounds.",
        )

    def test_action_potential_generation(self):
        """
        A suprathreshold stimulus (I_ext = 10 uA/cm^2) must drive the membrane
        above 0 mV, confirming that sodium channel activation can overcome the
        potassium and leak currents.
        """
        _, V = self.model.simulate(t_end=50.0, dt=0.01, I_ext=10.0)
        peak_voltage = np.max(V)
        self.assertGreater(
            peak_voltage,
            0.0,
            "FAIL: Membrane failed to fire an action potential under suprathreshold stimulation.",
        )

    def test_membrane_voltage_balance_equation(self):
        """
        Validates that dV/dt is computed correctly at a known state point.

        At rest (V = -65 mV) with gate variables at steady state and I_ext = 0,
        the net ionic current must balance to zero so that dV/dt ≈ 0.
        """
        V_rest = self.model.V_rest
        m0, h0, n0 = self.model._steady_state_gates(V_rest)
        dvdt = self.model.dVdt(V_rest, m0, h0, n0, I_ext=0.0)
        self.assertAlmostEqual(
            dvdt,
            0.0,
            places=1,
            msg="FAIL: dV/dt at resting steady state deviates from zero.",
        )

    def test_gate_variables_bounded(self):
        """
        Gate variables m, h, n represent probabilities and must remain in [0, 1]
        throughout the simulation to preserve physical meaning.
        """
        steps = int(50.0 / 0.01)
        dt = 0.01
        V = self.model.V_rest
        m, h, n = self.model._steady_state_gates(V)

        for _ in range(steps):
            dv = self.model.dVdt(V, m, h, n, I_ext=10.0)
            dm = self.model._alpha_m(V) * (1 - m) - self.model._beta_m(V) * m
            dh = self.model._alpha_h(V) * (1 - h) - self.model._beta_h(V) * h
            dn = self.model._alpha_n(V) * (1 - n) - self.model._beta_n(V) * n
            V += dt * dv
            m += dt * dm
            h += dt * dh
            n += dt * dn

        self.assertTrue(0.0 <= m <= 1.0, f"FAIL: Gate m={m:.4f} out of bounds [0, 1].")
        self.assertTrue(0.0 <= h <= 1.0, f"FAIL: Gate h={h:.4f} out of bounds [0, 1].")
        self.assertTrue(0.0 <= n <= 1.0, f"FAIL: Gate n={n:.4f} out of bounds [0, 1].")


if __name__ == "__main__":
    unittest.main()
