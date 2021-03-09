#!/usr/bin/env python

from . import compounds as cm
from . import reaction as rc

import numpy as np
import pandas as pd
from typing import Dict, List


class Network:
    """Defines a chemical network
    """
    def __init__(self):
        self.compounds: Dict = {}
        self.reactions: List = []
        self.rates: Dict = {}
        self.t_gas = 300

    def add_compound(self, name: str, density=0):
        """Add a compound to the chemical network

        :param name: name of the compound
        :param density: initial number density
        :return: None
        """
        self.compounds.update({name: cm.Compound(name, density=density)})

    def add_reaction(self, reactants: List[str], products: List[str], sigma, barrier=0., norm=1):
        """Add a reaction to the chemical network

        :param reactants: compounds that are consumed in the reaction
        :param products: compounds that are produced in the reaction
        :param sigma: reaction cross section
        :param barrier: thermal reaction barrier, for the Arrhenius equation
        :param norm: a normalization constant, mainly used for a reaction on multiple reactive sites
        :return: None
        """

        # Check if the reactants are already present in the network
        for reactant in reactants:
            if reactant not in self.compounds:
                self.add_compound(reactant)
        # Check if the products are already present in the network
        for product in products:
            if product not in self.compounds:
                self.add_compound(product)
        # Create a Reaction object, and add it to the network
        self.reactions.append(rc.Reaction(reactants=[self.compounds[reactant] for reactant in reactants],
                                          products=[self.compounds[product] for product in products],
                                          sigma=sigma,
                                          barrier=barrier,
                                          norm=norm
                                          ))

    def get_rates(self):
        """Calculate the rates for every reaction in the network

        :return: None
        """
        for reaction in self.reactions:
            self.rates.update({reaction: reaction.get_rate(t_gas=self.t_gas)})

    def apply_reactions(self, t_step: float = 1.e-3):
        """Apply all the reactions for a single step of length <t_step>

        :param t_step: length of the step
        :return: None
        """

        # Update all the reaction rates
        self.get_rates()
        # Cycle through all reactions
        for reaction in self.reactions:
            # Get the reaction rate
            reaction_rate = self.rates[reaction]
            # Decrease the density of every reactant with the product of reaction rate and step size
            for reactant in reaction.reactants:
                reactant.density -= reaction_rate * t_step
            # Increase the density of every product with the product of reaction rate and step size
            for product in reaction.products:
                product.density += reaction_rate * t_step

    def run_network(self, starting_density: Dict, t_step: float = 1.e-3, t_total: float = 1.) -> pd.DataFrame:
        """Run the entire network for a predetermined amount of time

        :param starting_density: starting densities for non-zero compounds
        :param t_step: the length of an individual step
        :param t_total: the total time for which to run the network
        :return: the number densities of all compounds throughout the time
        """

        # Create an array of timestamps
        time_steps = np.arange(0, t_total+t_step, t_step)

        # Set the initial densities of the non-zero compounds
        for compound in self.compounds.values():
            if compound.name in starting_density.keys():
                compound.density = starting_density[compound.name]
            else:
                compound.density = 0.

        # Create a dictionary with a list of densities per compound
        compound_densities = {compound.name: [compound.density] for compound in self.compounds.values()}

        # After every step, append the updated densities to the dictionary of compound densities
        for _ in time_steps[1:]:
            self.apply_reactions(t_step=t_step)
            for compound in self.compounds.values():
                compound_densities[compound.name].append(compound.density)

        # Add time to the dictionary
        compound_densities.update({'time': time_steps})

        # Convert the dictionary to an indexed dataframe, and return it
        return pd.DataFrame(data=compound_densities).set_index('time')
