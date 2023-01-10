import numpy as np
import Quantum


class RareEarthIon_DopedInCrystal:
    @staticmethod
    def Hamiltonian_odd(beta_e: float, beta_n: float, gn: float,
                        B: np.ndarray, A: np.ndarray, g: np.ndarray, Q: np.ndarray,
                        Ix: np.ndarray, Iy: np.ndarray, Iz: np.ndarray,
                        Sx: np.ndarray, Sy: np.ndarray, Sz: np.ndarray) -> np.ndarray:
        """
        :return: {np.ndarray: (16, 16)}
        """
        return RareEarthIon_DopedInCrystal.Ham_ez(beta_e, B, g, Sx, Sy, Sz) \
               + RareEarthIon_DopedInCrystal.Ham_hf(Ix, Iy, Iz, A, Sx, Sy, Sz) \
               + RareEarthIon_DopedInCrystal.Ham_q(Ix, Iy, Iz, Q) \
               - RareEarthIon_DopedInCrystal.Ham_nz(beta_n, gn, B, Ix, Iy, Iz)

    @staticmethod
    def Hamiltonian_even(beta_e: float, B: np.ndarray, g: np.ndarray, Sx: np.ndarray, Sy: np.ndarray,
                         Sz: np.ndarray) -> np.ndarray:
        """
        :return: {np.ndarray: (16, 16)}
        """
        return RareEarthIon_DopedInCrystal.Ham_ez(beta_e, B, g, Sx, Sy, Sz)

    @staticmethod
    def Ham_q(Ix: np.ndarray, Iy: np.ndarray, Iz: np.ndarray, Q: np.ndarray) -> np.ndarray:
        """
        :return: {np.ndarray: (16, 16)}
        """
        E2 = np.eye(2)
        return np.kron(RareEarthIon_DopedInCrystal.Hq(Q, Ix, Iy, Iz), E2)

    @staticmethod
    def Hq(Q, Ix, Iy, Iz) -> {np.ndarray: (8, 8)}:
        """
        :return: {np.ndarray: (8, 8)}
        """
        H0 = Q[0, 0] * Ix.dot(Ix) + Q[0, 1] * Ix.dot(Iy) + Q[0, 2] * Ix.dot(Iz)
        H1 = Q[1, 0] * Iy.dot(Ix) + Q[1, 1] * Iy.dot(Iy) + Q[1, 2] * Iy.dot(Iz)
        H2 = Q[2, 0] * Iz.dot(Ix) + Q[2, 1] * Iz.dot(Iy) + Q[2, 2] * Iz.dot(Iz)
        return H0 + H1 + H2

    @staticmethod
    def Ham_hf(Ix: np.ndarray, Iy: np.ndarray, Iz: np.ndarray, A: np.ndarray, Sx: np.ndarray, Sy: np.ndarray,
               Sz: np.ndarray) -> np.ndarray:
        """
        :return: {np.ndarray: (16, 16)}
        """
        return RareEarthIon_DopedInCrystal.Hhf(A, Ix, Iy, Iz, Sx, Sy, Sz)

    @staticmethod
    def Hhf(A, Ix, Iy, Iz, Sx, Sy, Sz) -> {np.ndarray: (16, 16)}:
        """
        :return: {np.ndarray: (16, 16)}
        """
        H0 = A[0, 0] * np.kron(Ix, Sx) + A[0, 1] * np.kron(Ix, Sy) + A[0, 2] * np.kron(Ix, Sz)
        H1 = A[1, 0] * np.kron(Iy, Sx) + A[1, 1] * np.kron(Iy, Sy) + A[1, 2] * np.kron(Iy, Sz)
        H2 = A[2, 0] * np.kron(Iz, Sx) + A[2, 1] * np.kron(Iz, Sy) + A[2, 2] * np.kron(Iz, Sz)
        return H0 + H1 + H2

    @staticmethod
    def Ham_ez(beta_e: float, B: np.ndarray, g: np.ndarray, Sx: np.ndarray, Sy: np.ndarray,
               Sz: np.ndarray) -> np.ndarray:
        """
        :return: {np.ndarray: (16, 16)}
        """
        E8 = np.eye(8)
        return np.kron(E8, RareEarthIon_DopedInCrystal.Hez(beta_e, B, g, Sx, Sy, Sz))

    @staticmethod
    def Hez(beta_e, B, g, Sx, Sy, Sz) -> {np.ndarray: (2, 2)}:
        """
        :return: {np.ndarray: (2, 2)}
        """
        H0: float = B[0] * (g[0, 0] * Sx + g[0, 1] * Sy + g[0, 2] * Sz)
        H1: float = B[1] * (g[1, 0] * Sx + g[1, 1] * Sy + g[1, 2] * Sz)
        H2: float = B[2] * (g[2, 0] * Sx + g[2, 1] * Sy + g[2, 2] * Sz)
        return beta_e * (H0 + H1 + H2)

    @staticmethod
    def Ham_nz(beta_n: float, gn: float, B: np.ndarray, Ix: np.ndarray, Iy: np.ndarray, Iz: np.ndarray) -> np.ndarray:
        """
        :return: {np.ndarray: (16, 16)}
        """
        E2 = np.eye(2)
        return np.kron(RareEarthIon_DopedInCrystal.Hnz(beta_n, B, gn,
                                                       Ix, Iy, Iz), E2)

    @staticmethod
    def Hnz(beta_n, B, gn, Ix, Iy, Iz) -> {np.ndarray: (8, 8)}:
        """
        :return: {np.ndarray: (8, 8)}
        """
        return -beta_n * gn * (B[0] * Ix + B[1] * Iy + B[2] * Iz)
