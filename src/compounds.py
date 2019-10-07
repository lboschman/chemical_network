#!/usr/bin/env python


class Compound:
    def __init__(self, name: str, density=0.):
        self._name = name
        self._density = density

    @property
    def name(self):
        return self._name

    @property
    def density(self):
        return self._density

    @density.setter
    def density(self, density):
        self._density = density
