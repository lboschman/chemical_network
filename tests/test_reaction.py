import compounds as chem
import reaction

cor = chem.Compound(name='Coronene', density=1)
hyd = chem.Compound(name='Hydrogen', density=1)
corh = chem.Compound(name='CorH', density=0)

test_reaction = reaction.Reaction([cor, hyd], [corh], sigma=1., barrier=0.)

print(test_reaction.get_rate())