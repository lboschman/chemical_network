#!/usr/bin/env python

import compounds as cm
import reaction as rc

import numpy as np
import pandas as pd
from typing import Dict, List


class Network:
    def __init__(self):
        self.compounds: Dict = None
        self.reactions: List = []
        self.rates: Dict = {}
        self.t_gas = 300

    def add_compound(self, name, density=0):
        if self.compounds is not None:
            self.compounds.update({name: cm.Compound(name, density=density)})
        else:
            self.compounds = {name: cm.Compound(name, density=density)}

    def add_reaction(self, reactants: List[str], products: List[str], sigma, barrier=0., norm=1):
        for reactant in reactants:
            if self.compounds is None or reactant not in self.compounds:
                self.add_compound(reactant)
        for product in products:
            if self.compounds is None or product not in self.compounds:
                self.add_compound(product)
        self.reactions.append(rc.Reaction(reactants=[self.compounds[reactant] for reactant in reactants],
                                          products=[self.compounds[product] for product in products],
                                          sigma=sigma,
                                          barrier=barrier,
                                          norm=norm
                                          ))

    def get_rates(self):
        for reaction in self.reactions:
            self.rates.update({reaction: reaction.get_rate(t_gas=self.t_gas)})

    def apply_reactions(self, t_step: float = 1.e-3):
        self.get_rates()
        for reaction in self.reactions:
            reaction_rate = self.rates[reaction]
            for reactant in reaction.reactants:
                reactant.density -= reaction_rate * t_step
            for product in reaction.products:
                product.density += reaction_rate * t_step

    def run_network(self, starting_density: Dict, t_step: float = 1.e-3, t_total: float = 1.):
        time_steps = np.arange(0, t_total+t_step, t_step)

        for compound in self.compounds.values():
            if compound.name in starting_density.keys():
                compound.density = starting_density[compound.name]
            else:
                compound.density = 0.

        compound_densities = {compound.name: [compound.density] for compound in self.compounds.values()}

        for step in time_steps[1:]:
            self.apply_reactions(t_step=t_step)
            for compound in self.compounds.values():
                compound_densities[compound.name].append(compound.density)

        compound_densities.update({'time': time_steps})

        return pd.DataFrame(data=compound_densities).set_index('time')




