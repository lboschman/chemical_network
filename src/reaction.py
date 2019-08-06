#!/usr/bin/env python

import numpy as np
import scipy as sc
from scipy.constants import Boltzmann


class Reaction:
    def __init__(self, reactants, products, sigma, barrier, norm=1):
        self.reactants = reactants
        self.products = products
        self.sigma = sigma
        self.barrier = barrier
        self.norm = norm

    def get_rate(self, t_gas=300):
        concentration = 1
        for product in self.products:
            concentration *= product.density
        return self.norm * concentration * self.sigma * np.exp(- self.barrier/(Boltzmann * t_gas))




