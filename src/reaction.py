#!/usr/bin/env python

import compounds

import numpy as np
import scipy as sc
from scipy.constants import Boltzmann

from typing import List


class Reaction:
    def __init__(self, reactants: List[compounds.Compound], products: List[compounds.Compound],
                 sigma: float, barrier: float, norm: float=1):
        self.reactants = reactants
        self.products = products
        self.sigma = sigma
        self.barrier = barrier
        self.norm = norm

    def get_rate(self, t_gas=300):
        concentration = 1
        for reactant in self.reactants:
            concentration *= reactant.density
        return self.norm * concentration * self.sigma * np.exp(- self.barrier/(Boltzmann * t_gas))




