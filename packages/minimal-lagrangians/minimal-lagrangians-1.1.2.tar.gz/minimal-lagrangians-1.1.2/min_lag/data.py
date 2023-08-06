from fractions import Fraction
from .fields import FermionField, ScalarField
from .models import BSMModel


# particles’ hypercharges are given relative to a free parameter α
# (i.e. the total hypercharge is <hypercharge> + α)
DATA_LIST = [
	# List of models contained within
	# https://arxiv.org/abs/1308.3655
	# T1-1
	BSMModel('T1-1-A', (
		ScalarField ("φ",  1, Y= 0),
		ScalarField ("ϕ'", 2, Y=-1),
		FermionField("ψ",  1, Y= 0),
		ScalarField ("ϕ",  2, Y= 1),
	), (0, 2)), # α = -2 is equivalent to α = 2
	BSMModel('T1-1-B', (
		ScalarField ("φ",  1, Y= 0),
		ScalarField ("ϕ'", 2, Y=-1),
		FermionField("ψ",  3, Y= 0),
		ScalarField ("ϕ",  2, Y= 1),
	), (0, 2)), # α = -2 is equivalent to α = 2
	BSMModel('T1-1-C', (
		ScalarField ("φ",  2, Y= 0),
		ScalarField ("ϕ'", 1, Y=-1),
		FermionField("ψ",  2, Y= 0),
		ScalarField ("ϕ",  1, Y= 1),
	), (1,)), # α = -1 is equivalent to α = 1
	BSMModel('T1-1-D', (
		ScalarField ("φ",  2, Y= 0),
		ScalarField ("ϕ'", 1, Y=-1),
		FermionField("ψ",  2, Y= 0),
		ScalarField ("ϕ",  3, Y= 1),
	), (-3, -1, 1)), # α = -3 excluded by direct detection
	BSMModel('T1-1-E', (
		ScalarField ("φ",  2, Y= 0),
		ScalarField ("ϕ'", 3, Y=-1),
		FermionField("ψ",  2, Y= 0),
		ScalarField ("ϕ",  1, Y= 1),
	), (-1, 1, 3)), # α = -1 equivalent to T1-1-D (α = 1);
	                # α = 1 equivalent to T1-1-D (α = -1);
	                # α = 3 excluded by direct detection
	BSMModel('T1-1-F', (
		ScalarField ("φ",  2, Y= 0),
		ScalarField ("ϕ'", 3, Y=-1),
		FermionField("ψ",  2, Y= 0),
		ScalarField ("ϕ",  3, Y= 1),
	), (1, 3)), # α = -1 is equivalent to α = 1;
	            # α = -3 is equivalent to α = 3;
	            # |α| = 3 excluded by direct detection
	BSMModel('T1-1-G', (
		ScalarField ("φ",  3, Y= 0),
		ScalarField ("ϕ'", 2, Y=-1),
		FermionField("ψ",  1, Y= 0),
		ScalarField ("ϕ",  2, Y= 1),
	), (0, 2)), # α = -2 is equivalent to α = 2
	BSMModel('T1-1-H', (
		ScalarField ("φ",  3, Y= 0),
		ScalarField ("ϕ'", 2, Y=-1),
		FermionField("ψ",  3, Y= 0),
		ScalarField ("ϕ",  2, Y= 1),
	), (0, 2)), # α = -2 is equivalent to α = 2
	# T1-2
	BSMModel('T1-2-A', (
		FermionField("ψ",  1, Y= 0),
		ScalarField ("ϕ",  2, Y= 1),
		ScalarField ("ϕ'", 1, Y= 0),
		FermionField("ψ'", 2, Y= 1),
	), (-2, 0)),
	BSMModel('T1-2-B', (
		FermionField("ψ",  1, Y= 0),
		ScalarField ("ϕ",  2, Y= 1),
		ScalarField ("ϕ'", 3, Y= 0),
		FermionField("ψ'", 2, Y= 1),
	), (-2, 0, 2)), # α = 2 excluded by direct detection
	BSMModel('T1-2-C', (
		FermionField("ψ",  2, Y= 0),
		ScalarField ("ϕ",  1, Y= 1),
		ScalarField ("ϕ'", 2, Y= 0),
		FermionField("ψ'", 1, Y= 1),
	), (-1, 1)), # α = -1 equivalent to T1-2-A (α = 0);
	             # α = 1 equivalent to T1-2-A (α = -2);
	BSMModel('T1-2-D', (
		FermionField("ψ",  2, Y= 0),
		ScalarField ("ϕ",  1, Y= 1),
		ScalarField ("ϕ'", 2, Y= 0),
		FermionField("ψ'", 3, Y= 1),
	), (-3, -1, 1)), # α = -3 not consistent with dark matter
	BSMModel('T1-2-E', (
		FermionField("ψ",  2, Y= 0),
		ScalarField ("ϕ",  3, Y= 1),
		ScalarField ("ϕ'", 2, Y= 0),
		FermionField("ψ'", 1, Y= 1),
	), (-3, -1, 1)), # α = -3 excluded by direct detection;
	                 # α = -1 equivalent to T1-2-B (α = 0);
	                 # α = 1 equivalent to T1-2-B (α = -2)
	BSMModel('T1-2-F', (
		FermionField("ψ",  2, Y= 0),
		ScalarField ("ϕ",  3, Y= 1),
		ScalarField ("ϕ'", 2, Y= 0),
		FermionField("ψ'", 3, Y= 1),
	), (-3, -1, 1)), # α = -3 not consistent with dark matter
	BSMModel('T1-2-G', (
		FermionField("ψ",  3, Y= 0),
		ScalarField ("ϕ",  2, Y= 1),
		ScalarField ("ϕ'", 1, Y= 0),
		FermionField("ψ'", 2, Y= 1),
	), (-2, 0, 2)), # α = -2 equivalent to T1-2-D (α = 1);
	                # α = 0 equivalent to T1-2-D (α = -1);
	                # α = 2 excluded by direct detection
	BSMModel('T1-2-H', (
		FermionField("ψ",  3, Y= 0),
		ScalarField ("ϕ",  2, Y= 1),
		ScalarField ("ϕ'", 3, Y= 0),
		FermionField("ψ'", 2, Y= 1),
	), (-2, 0, 2)), # α = -2 equivalent to T1-2-F (α = 1);
	                # α = 0 equivalent to T1-2-F (α = -1);
	                # α = 2 excluded by direct detection
	# T1-3
	BSMModel('T1-3-A', (
		FermionField("Ψ",  1, Y= 0),
		FermionField("ψ'", 2, Y= 1),
		ScalarField ("ϕ",  1, Y= 0),
		FermionField("ψ",  2, Y=-1),
	), (0, 2)), # α = -2 is equivalent to α = 2
	            # |α| = 2 excluded by direct detection
	BSMModel('T1-3-B', (
		FermionField("Ψ",  1, Y= 0),
		FermionField("ψ'", 2, Y= 1),
		ScalarField ("ϕ",  3, Y= 0),
		FermionField("ψ",  2, Y=-1),
	), (0, 2)), # α = -2 is equivalent to α = 2
	            # |α| = 2 excluded by direct detection
	BSMModel('T1-3-C', (
		FermionField("Ψ",  2, Y= 0),
		FermionField("ψ'", 1, Y= 1),
		ScalarField ("ϕ",  2, Y= 0),
		FermionField("ψ",  1, Y=-1),
	), (1,)), # α = -1 is equivalent to α = 1
	BSMModel('T1-3-D', (
		FermionField("Ψ",  2, Y= 0),
		FermionField("ψ'", 1, Y= 1),
		ScalarField ("ϕ",  2, Y= 0),
		FermionField("ψ",  3, Y=-1),
	), (-1, 1, 3)), # α = 3 excluded by direct detection
	BSMModel('T1-3-E', (
		FermionField("Ψ",  2, Y= 0),
		FermionField("ψ'", 3, Y= 1),
		ScalarField ("ϕ",  2, Y= 0),
		FermionField("ψ",  1, Y=-1),
	), (-1, 1, 3)), # α = -3 excluded by direct detection;
	                # α = -1 equivalent to T1-3-D (α = 1);
	                # α = 1 equivalent to T1-3-D (α = -1)
	BSMModel('T1-3-F', (
		FermionField("Ψ",  2, Y= 0),
		FermionField("ψ'", 3, Y= 1),
		ScalarField ("ϕ",  2, Y= 0),
		FermionField("ψ",  3, Y=-1),
	), (1, 3)), # α = -3 is equivalent α = 3;
	            # α = -1 is equivalent α = 1;
                # |α| = 3 excluded by direct detection
	BSMModel('T1-3-G', (
		FermionField("Ψ",  3, Y= 0),
		FermionField("ψ'", 2, Y= 1),
		ScalarField ("ϕ",  1, Y= 0),
		FermionField("ψ",  2, Y=-1),
	), (0, 2)), # α = -2 is equivalent α = 2;
                # |α| = 2 excluded by direct detection
	BSMModel('T1-3-H', (
		FermionField("Ψ",  3, Y= 0),
		FermionField("ψ'", 2, Y= 1),
		ScalarField ("ϕ",  3, Y= 0),
		FermionField("ψ",  2, Y=-1),
	), (0, 2)), # α = -2 is equivalent α = 2;
                # |α| = 2 excluded by direct detection
	# T3
	BSMModel('T3-A', (
		ScalarField ("ϕ'", 1, Y= 0),
		ScalarField ("ϕ",  3, Y= 2),
		FermionField("ψ",  2, Y= 1),
	), (-4, -2, 0)), # α = -4 excluded by direct detection
	BSMModel('T3-B', (
		ScalarField ("ϕ'", 2, Y= 0),
		ScalarField ("ϕ",  2, Y= 2),
		FermionField("ψ",  1, Y= 1),
	), (-1, 1)), # α = -3 is equivalent α = 1
	BSMModel('T3-C', (
		ScalarField ("ϕ'", 2, Y= 0),
		ScalarField ("ϕ",  2, Y= 2),
		FermionField("ψ",  3, Y= 1),
	), (-1, 1)), # α = -3 is equivalent α = 1
	BSMModel('T3-D', (
		ScalarField ("ϕ'", 3, Y= 0),
		ScalarField ("ϕ",  1, Y= 2),
		FermionField("ψ",  2, Y= 1),
	), (-2, 0, 2)), # α = -2 equivalent to T3-A (α = 0);
	                # α = 0 equivalent to T3-A (α = -2);
                    # α = 2 excluded by direct detection
	BSMModel('T3-E', (
		ScalarField ("ϕ'", 3, Y= 0),
		ScalarField ("ϕ",  3, Y= 2),
		FermionField("ψ",  2, Y= 1),
	), (0, 2)), # α = -4 is equivalent α = 2;
                # α = -2 is equivalent α = 0;
                # α = 2 not consistent with dark matter

	# Models from https://arxiv.org/abs/1311.5896
	# (note that the paper uses a different definition of the hypercharge:
	# Y' = Y/2)
	# Model A: singlet-doublet fermion
	BSMModel('SDF', (
		FermionField('S',   1, Y= 0),
		FermionField('D_1', 2, Y=-1),
		FermionField('D_2', 2, Y= 1),
	)),
	# Model B: singlet-doublet scalar
	BSMModel('SDS', (
		ScalarField ('S',   1, Y= 0),
		ScalarField ('D',   2, Y= 1),
	)),
	# Model C: singlet-triplet scalar
	BSMModel('STS', (
		ScalarField ('S',   1, Y= 0),
		ScalarField ('T',   3, Y= 0),
	)),

	# Higgs triplet model
	BSMModel('Higgs-triplet', (
		ScalarField ('Δ', 3, Y=2, z2=1),
	)),
	# Seesaw type I
	BSMModel('SeesawI', (
		FermionField('N', 1, Y=0, z2=1),
	)),
	# Seesaw type II
	BSMModel('SeesawII', (
		ScalarField ('Δ', 3, Y=2, z2=1),
	)),
	# Seesaw type III
	BSMModel('SeesawIII', (
		FermionField('Σ', 3, Y=0, z2=1),
	)),

	# scalar singlet (Higgs portal)
	BSMModel('SSDM', (
		ScalarField ('S', 1, Y=0, z2=1),
	)),

	# T1-3-B (α = 0) with 2 generations of scalar triplets
	BSMModel('T1-3-B_0_2g', (
		FermionField("Ψ",   1, Y= 0),
		FermionField("ψ'",  2, Y= 1),
		ScalarField ("ϕ1",  3, Y= 0),
		ScalarField ("ϕ2",  3, Y= 0),
		FermionField("ψ",   2, Y=-1),
	)),
	# T1-3-B (α = 0) without ℤ₂
	BSMModel('T1-3-B_0_even', (
		FermionField("Ψ",  1, Y= 0, z2=1),
		FermionField("ψ'", 2, Y= 1, z2=1),
		ScalarField ("ϕ",  3, Y= 0, z2=1),
		FermionField("ψ",  2, Y=-1, z2=1),
	)),
]

def append(data_list):
	DATA.update({model.name: model for model in data_list})

DATA = {}
append(DATA_LIST)

