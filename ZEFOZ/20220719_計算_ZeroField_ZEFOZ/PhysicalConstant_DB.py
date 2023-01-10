from scipy.constants import physical_constants
from scipy.constants import pi
import numpy as np


class PhysicalConstant_DB:
    muB: float = physical_constants['Bohr magneton in eV/T'][0]
    muN: float = physical_constants['nuclear magneton in eV/T'][0]
    hbar: float = physical_constants['Planck constant over 2 pi in eV s'][0]

    # E=hνのνが知りたいので，事前にhで割っておく
    beta_e: float = muB / hbar / 2 / pi
    beta_n: float = muN / hbar / 2 / pi


if __name__ == '__main__':
    print(PhysicalConstant_DB.muB)
    print(PhysicalConstant_DB.muN)
    print(PhysicalConstant_DB.hbar)
    print(PhysicalConstant_DB.beta_e)
    print(PhysicalConstant_DB.beta_n)
