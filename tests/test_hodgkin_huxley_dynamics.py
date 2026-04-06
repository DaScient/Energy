import unittest
import numpy as np


def _alpha_m(V):
    """Sodium activation rate (handles singularity at V=-40)."""
    dv = V + 40.0
    if abs(dv) < 1e-7:
        return 1.0
    return 0.1 * dv / (1.0 - np.exp(-dv / 10.0))


def _beta_m(V):
    return 4.0 * np.exp(-(V + 65.0) / 18.0)


def _alpha_h(V):
    return 0.07 * np.exp(-(V + 65.0) / 20.0)


def _beta_h(V):
    return 1.0 / (1.0 + np.exp(-(V + 35.0) / 10.0))


def _alpha_n(V):
    """Potassium activation rate (handles singularity at V=-55)."""
    dv = V + 55.0
    if abs(dv) < 1e-7:
        return 0.1
    return 0.01 * dv / (1.0 - np.exp(-dv / 10.0))


def _beta_n(V):
    return 0.125 * np.exp(-(V + 65.0) / 80.0)


def steady_state_gates(V):
    """Return (m_inf, h_inf, n_inf) at a given membrane potential."""
    am, bm = _alpha_m(V), _beta_m(V)
    ah, bh = _alpha_h(V), _beta_h(V)
    an, bn = _alpha_n(V), _beta_n(V)
    m = am / (am + bm)
    h = ah / (ah + bh)
    n = an / (an + bn)
    return m, h, n


def simulate_hh(I_ext_uA_cm2, duration_ms=50.0, dt=0.01):
    """
    Numerically integrate the Hodgkin-Huxley model using forward Euler.

    C_m * dV/dt = I_ext - g_Na*m^3*h*(V-E_Na) - g_K*n^4*(V-E_K) - g_L*(V-E_L)

    Parameters
    ----------
    I_ext_uA_cm2 : float
        Constant applied current (μA/cm²).
    duration_ms : float
        Simulation duration (ms).
    dt : float
        Time step (ms).

    Returns
    -------
    t : np.ndarray  Time vector (ms).
    V : np.ndarray  Membrane potential (mV).
    """
    # Standard HH parameters
    C_m = 1.0      # μF/cm²
    g_Na = 120.0   # mS/cm²
    g_K = 36.0     # mS/cm²
    g_L = 0.3      # mS/cm²
    E_Na = 50.0    # mV
    E_K = -77.0    # mV
    E_L = -54.387  # mV
    V_rest = -65.0 # mV

    steps = int(duration_ms / dt)
    t = np.zeros(steps)
    V_arr = np.zeros(steps)

    V = V_rest
    m, h, n = steady_state_gates(V_rest)

    for i in range(steps):
        t[i] = i * dt
        V_arr[i] = V

        I_Na = g_Na * m**3 * h * (V - E_Na)
        I_K = g_K * n**4 * (V - E_K)
        I_L = g_L * (V - E_L)

        dV = (I_ext_uA_cm2 - I_Na - I_K - I_L) / C_m
        dm = _alpha_m(V) * (1 - m) - _beta_m(V) * m
        dh = _alpha_h(V) * (1 - h) - _beta_h(V) * h
        dn = _alpha_n(V) * (1 - n) - _beta_n(V) * n

        V += dV * dt
        m += dm * dt
        h += dh * dt
        n += dn * dt

    return t, V_arr


class TestHodgkinHuxleyDynamics(unittest.TestCase):
    """
    Validates membrane voltage balance for the Hodgkin-Huxley model:
    C_m * dV/dt = I_ext - g_Na*m^3*h*(V - E_Na) - g_K*n^4*(V - E_K) - g_L*(V - E_L)
    """

    def test_resting_potential_stability(self):
        """
        With zero applied current the membrane potential must remain near the
        resting value (-65 mV) and must not drift beyond physiological bounds.
        """
        _, V = simulate_hh(I_ext_uA_cm2=0.0, duration_ms=50.0)
        self.assertTrue(
            np.all(np.abs(V - (-65.0)) < 5.0),
            "FAIL: Resting membrane potential drifted beyond ±5 mV of -65 mV."
        )

    def test_action_potential_generation(self):
        """
        A suprathreshold stimulus (10 μA/cm²) must drive the membrane above
        0 mV, confirming that the ionic conductances produce a proper action
        potential.
        """
        _, V = simulate_hh(I_ext_uA_cm2=10.0, duration_ms=50.0)
        self.assertTrue(
            np.max(V) > 0.0,
            "FAIL: No action potential generated; peak voltage did not exceed 0 mV."
        )

    def test_subthreshold_no_spike(self):
        """
        A subthreshold stimulus (0.5 μA/cm²) must not elicit a full action
        potential (peak should stay below 0 mV).
        """
        _, V = simulate_hh(I_ext_uA_cm2=0.5, duration_ms=50.0)
        self.assertTrue(
            np.max(V) < 0.0,
            "FAIL: Subthreshold current erroneously produced an action potential."
        )

    def test_membrane_voltage_balance_equation(self):
        """
        Spot-check the right-hand side of:
        C_m * dV/dt = I_ext - g_Na*m^3*h*(V-E_Na) - g_K*n^4*(V-E_K) - g_L*(V-E_L)
        at resting potential with zero current; the net ionic drive must be ≈ 0.
        """
        C_m = 1.0
        g_Na, g_K, g_L = 120.0, 36.0, 0.3
        E_Na, E_K, E_L = 50.0, -77.0, -54.387
        V = -65.0
        I_ext = 0.0

        m, h, n = steady_state_gates(V)

        I_Na = g_Na * m**3 * h * (V - E_Na)
        I_K = g_K * n**4 * (V - E_K)
        I_L = g_L * (V - E_L)

        dV_dt = (I_ext - I_Na - I_K - I_L) / C_m

        self.assertAlmostEqual(
            dV_dt, 0.0, delta=0.5,
            msg="FAIL: Membrane voltage balance at rest deviates from zero."
        )

    def test_physiological_voltage_range(self):
        """
        Throughout a simulated action potential the membrane voltage must stay
        within the physiological window [-90 mV, +60 mV].
        """
        _, V = simulate_hh(I_ext_uA_cm2=10.0, duration_ms=50.0)
        self.assertTrue(
            np.all(V >= -90.0) and np.all(V <= 60.0),
            "FAIL: Membrane voltage exceeded physiological bounds [-90, +60] mV."
        )


if __name__ == '__main__':
    unittest.main()
