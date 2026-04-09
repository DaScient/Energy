import numpy as np


class HodgkinHuxleyModel:
    """
    Implements the Hodgkin-Huxley conductance-based neuron model.

    Membrane voltage dynamics are governed by:
        C_m * dV/dt = I_ext - g_Na*m^3*h*(V - E_Na)
                             - g_K*n^4*(V - E_K)
                             - g_L*(V - E_L)

    Gate variables m, h, n evolve according to their respective
    alpha/beta opening and closing rate functions.
    """

    def __init__(
        self,
        C_m: float = 1.0,       # membrane capacitance (uF/cm^2)
        g_Na: float = 120.0,    # max sodium conductance (mS/cm^2)
        g_K: float = 36.0,      # max potassium conductance (mS/cm^2)
        g_L: float = 0.3,       # leak conductance (mS/cm^2)
        E_Na: float = 50.0,     # sodium reversal potential (mV)
        E_K: float = -77.0,     # potassium reversal potential (mV)
        E_L: float = -54.387,   # leak reversal potential (mV)
        V_rest: float = -65.0,  # resting membrane potential (mV)
    ):
        self.C_m = C_m
        self.g_Na = g_Na
        self.g_K = g_K
        self.g_L = g_L
        self.E_Na = E_Na
        self.E_K = E_K
        self.E_L = E_L
        self.V_rest = V_rest

    # ------------------------------------------------------------------
    # Alpha/beta rate functions for gate variables
    # ------------------------------------------------------------------

    def _alpha_m(self, V: float) -> float:
        dv = V + 40.0
        if abs(dv) < 1e-7:
            return 1.0
        return 0.1 * dv / (1.0 - np.exp(-dv / 10.0))

    def _beta_m(self, V: float) -> float:
        return 4.0 * np.exp(-(V + 65.0) / 18.0)

    def _alpha_h(self, V: float) -> float:
        return 0.07 * np.exp(-(V + 65.0) / 20.0)

    def _beta_h(self, V: float) -> float:
        return 1.0 / (1.0 + np.exp(-(V + 35.0) / 10.0))

    def _alpha_n(self, V: float) -> float:
        dv = V + 55.0
        if abs(dv) < 1e-7:
            return 0.1
        return 0.01 * dv / (1.0 - np.exp(-dv / 10.0))

    def _beta_n(self, V: float) -> float:
        return 0.125 * np.exp(-(V + 65.0) / 80.0)

    # ------------------------------------------------------------------
    # Steady-state initial conditions
    # ------------------------------------------------------------------

    def _steady_state_gates(self, V: float):
        am = self._alpha_m(V)
        bm = self._beta_m(V)
        ah = self._alpha_h(V)
        bh = self._beta_h(V)
        an = self._alpha_n(V)
        bn = self._beta_n(V)
        m0 = am / (am + bm)
        h0 = ah / (ah + bh)
        n0 = an / (an + bn)
        return m0, h0, n0

    # ------------------------------------------------------------------
    # dV/dt computation
    # ------------------------------------------------------------------

    def dVdt(self, V: float, m: float, h: float, n: float, I_ext: float) -> float:
        """
        Returns dV/dt according to:
            C_m * dV/dt = I_ext - I_Na - I_K - I_L
        """
        I_Na = self.g_Na * m ** 3 * h * (V - self.E_Na)
        I_K = self.g_K * n ** 4 * (V - self.E_K)
        I_L = self.g_L * (V - self.E_L)
        return (I_ext - I_Na - I_K - I_L) / self.C_m

    # ------------------------------------------------------------------
    # Forward Euler integrator
    # ------------------------------------------------------------------

    def simulate(self, t_end: float = 50.0, dt: float = 0.01, I_ext: float = 10.0):
        """
        Integrates the HH equations over [0, t_end] ms using Forward Euler.

        Returns
        -------
        t  : 1-D ndarray of time points (ms)
        V  : 1-D ndarray of membrane voltages (mV)
        """
        steps = int(t_end / dt)
        t = np.arange(steps) * dt

        V = np.empty(steps)
        m_arr = np.empty(steps)
        h_arr = np.empty(steps)
        n_arr = np.empty(steps)

        V[0] = self.V_rest
        m_arr[0], h_arr[0], n_arr[0] = self._steady_state_gates(self.V_rest)

        for i in range(steps - 1):
            Vi, mi, hi, ni = V[i], m_arr[i], h_arr[i], n_arr[i]

            dv = self.dVdt(Vi, mi, hi, ni, I_ext)
            dm = self._alpha_m(Vi) * (1 - mi) - self._beta_m(Vi) * mi
            dh = self._alpha_h(Vi) * (1 - hi) - self._beta_h(Vi) * hi
            dn = self._alpha_n(Vi) * (1 - ni) - self._beta_n(Vi) * ni

            V[i + 1] = Vi + dt * dv
            m_arr[i + 1] = mi + dt * dm
            h_arr[i + 1] = hi + dt * dh
            n_arr[i + 1] = ni + dt * dn

        return t, V
