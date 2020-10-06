#!/usr/bin/env python

import compounds

import numpy as np
from scipy.constants import Boltzmann
from typing import List


class Reaction:
    """A reaction that follows Arrhenius kinetics (https://en.wikipedia.org/wiki/Arrhenius_equation).

    """
    def __init__(self, reactants: List[compounds.Compound], products: List[compounds.Compound],
                 sigma: float, barrier: float, norm: float = 1):
        """Initiate the reaction.

        :param reactants: reactants in the reaction
        :param products:  products in the reaction
        :param sigma: the reaction cross section
        :param barrier: the Arrhenius barrier
        :param norm: if there is a degeneracy to rescale the reaction cross section
        """
        self.reactants = reactants
        self.products = products
        self.sigma = sigma
        self.barrier = barrier
        self.norm = norm

    def get_rate(self, t_gas: float = 300.) -> float:
        """Calculate the reaction rate.

        :param t_gas: the gas temperature for the Arrhenius equation
        :return: the reaction rate
        """
        concentration = 1
        for reactant in self.reactants:
            concentration *= reactant.density
        return self.norm * concentration * self.sigma * np.exp(- self.barrier/(Boltzmann * t_gas))
