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

print(chemical_network.run_network({'Enzyme': 1, 'Substrate': 10}))

