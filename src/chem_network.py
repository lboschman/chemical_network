#!/usr/bin/env python

import compounds as cm
import reaction as rc

from typing import Dict, List


class Network:
    def __init__(self):
        self.compounds: Dict = None
        self.reactions: List = []

    def add_compound(self, name, density=0):
        if self.compounds is not None:
            self.compounds.update({name: cm.Compound(name, density=density)})
        else:
            self.compounds = {name: cm.Compound(name, density=density)}

    def add_reaction(self, reactants, products, sigma, norm=1):
        if self.reactions is not None:
            self.reactions.append(rc.Reaction(reactants=reactants,
                                              products=products,
                                              sigma=sigma,
                                              norm=norm
                                              ))


