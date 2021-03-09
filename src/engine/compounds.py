#!/usr/bin/env python


class Compound:
    """A chemical compound in the network, as a name and a number density

    """
    def __init__(self, name: str, density=0.):
        self._name = name
        self._density = density

    @property
    def name(self):
        """The name of the compound"""
        return self._name

    @property
    def density(self):
        """The number density of the compound"""
        return self._density

    @density.setter
    def density(self, density: float):
        self._density = density
