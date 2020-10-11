# Chemical network

This is a small project to visualize concentration variations while a chemical network is converging to a dynamical equilibrium.
The reactions in chemical network are all supposed to follow Arrhenius kinetics.


# Reactions
Reactions follow the [Arrhenius kinetic equation](https://en.wikipedia.org/wiki/Arrhenius_equation).
Reactions are specified by 4 things.

1. Reactants, the compounds that are reacting;
2. Products, the outcome of the reaction;
3. A rate constant, the _k_ in the Arrhenius equation;
4. An energy barrier, the _E<sub>a</sub>_ in the Arrhenius equation.

These reactions can be specified in a reaction file.
The most straight-forward way in this package is by supplying a fixed width text file.
It must have the following column names: 

- Reactants
- Products
- Sigma
- Barrier

A sample file would look like (__N.B. these numbers are made up!__):

```
Reactants              Products              Sigma        Barrier
C O2                   CO2                   2.           0.5
Ti O2                  TiO2                  1.5          0.8
```
If we want to add the reaction of methane (CH4) and oxygen, we need multiple oxygen molecules, and it 
produces multiple water molecules:

```
Reactants              Products              Sigma        Barrier
C O2                   CO2                   2.           0.5
Ti O2                  TiO2                  1.5          0.8
CH4 O2 O2              CO2 H2O H2O           2.1          0.9
```



