import matplotlib as mpl
from matplotlib import pyplot as plt

import chem_network as cn

f = open('../data/test_reactions.txt', 'r')
lines = f.readlines()
header = lines.pop(0)
reactant_index = 0
product_index = header.index('Products')
sigma_index = header.index('Sigma')
barrier_index = header.index('Barrier')

chemical_network = cn.Network()

for line in lines:
    chemical_network.add_reaction(reactants=line[reactant_index:product_index].split(),
                                  products=line[product_index:sigma_index].split(),
                                  sigma=float(line[sigma_index:barrier_index].strip(' \n')),
                                  barrier=float(line[barrier_index:-1].strip(' \n'))
                                  )

react_df = chemical_network.run_network({'Enzyme': 1, 'Substrate': 10}, t_total=60)

# react_df = react_df.set_index('time')

# fig = plt.figure()
# cols = list(react_df.columns)

react_df.plot()
plt.show()
plt.close()

# react_df.plot(list(react_df.columns))
# plt.savefig('testplot.png', format='png')
# plt.close()

