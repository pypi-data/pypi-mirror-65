#!/usr/bin/env python3
import collections
import unittest
import min_lag.terms
from min_lag.models import *


min_lag.terms.InvariantProduct.__repr__ = min_lag.terms.InvariantProduct.__str__
min_lag.terms.InvariantTerm.__repr__ = min_lag.terms.InvariantTerm.__str__

IP = min_lag.terms.InvariantProduct
IT = min_lag.terms.InvariantTerm


class Test(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		from min_lag.data import DATA
		cls.DATA = DATA
		cls.SCALAR_SINGLET  = ScalarField ('ss', 1, 0, z2=1)
		cls.SCALAR_DOUBLET  = ScalarField ('sd', 2, 0, z2=1)
		cls.SCALAR_TRIPLET  = ScalarField ('st', 3, 0, z2=1)
		cls.FERMION_SINGLET = FermionField('fs', 1, 0, z2=1)
		cls.FERMION_DOUBLET = FermionField('fd', 2, 0, z2=1)
		cls.FERMION_TRIPLET = FermionField('ft', 3, 0, z2=1)
		models_imp = [
			model.implement(alpha)
			for model in DATA.values()
			for alpha in model.param_values
		]
		cls.lagrangians = {
			model: model.lagrangian() for model in models_imp
		}

	def test_Field_components(self):
		Dn = ScalarField('Dn', 2, Y=0)
		Dc = ScalarField('Dc', 2, Y=1)
		Tn = ScalarField('Tn', 3, Y=0)
		Tc = ScalarField('Tc', 3, Y=2)
		comp = Dn.components
		self.assertFalse(Dn.real)
		self.assertEqual(comp[0], comp[1].adjoint)
		self.assertEqual(comp[0].charge, Fraction('1/2'))
		self.assertEqual(comp[1].charge, Fraction('-1/2'))
		with self.assertRaises(ValueError) as _: comp[0].complex_parts
		with self.assertRaises(ValueError) as _: comp[1].complex_parts
		comp = Dc.components
		self.assertFalse(Dc.real)
		self.assertNotEqual(comp[0], comp[1].adjoint)
		self.assertEqual(comp[0].charge, 1)
		self.assertEqual(comp[1].charge, 0)
		with self.assertRaises(ValueError) as _: comp[0].complex_parts
		self.assertTrue(comp[1].neutral)
		self.assertFalse(comp[1].real)
		scalar, pseudoscalar = comp[1].complex_parts
		self.assertEqual(scalar.charge, 0)
		self.assertEqual(pseudoscalar.charge, 0)
		self.assertTrue(scalar.neutral)
		self.assertTrue(pseudoscalar.neutral)
		self.assertTrue(scalar.real)
		self.assertTrue(pseudoscalar.real)
		comp = Tn.components
		self.assertTrue(Tn.real)
		self.assertEqual(comp[0], comp[2].adjoint)
		self.assertEqual(comp[0].charge, 1)
		self.assertEqual(comp[1].charge, 0)
		self.assertEqual(comp[2].charge, -1)
		with self.assertRaises(ValueError) as _: comp[0].complex_parts
		with self.assertRaises(ValueError) as _: comp[2].complex_parts
		self.assertTrue(comp[1].neutral)
		self.assertTrue(comp[1].real)
		scalar, pseudoscalar = comp[1].complex_parts
		self.assertEqual(pseudoscalar, 0)
		self.assertEqual(scalar.charge, 0)
		self.assertTrue(scalar.neutral)
		self.assertTrue(scalar.real)
		comp = Tc.components
		self.assertFalse(Tc.real)
		self.assertEqual(comp[0].charge, 2)
		self.assertEqual(comp[1].charge, 1)
		self.assertEqual(comp[2].charge, 0)
		with self.assertRaises(ValueError) as _: comp[0].complex_parts
		with self.assertRaises(ValueError) as _: comp[1].complex_parts
		self.assertTrue(comp[2].neutral)
		self.assertFalse(comp[2].real)
		scalar, pseudoscalar = comp[2].complex_parts
		self.assertEqual(scalar.charge, 0)
		self.assertEqual(pseudoscalar.charge, 0)
		self.assertTrue(scalar.neutral)
		self.assertTrue(pseudoscalar.neutral)
		self.assertTrue(scalar.real)
		self.assertTrue(pseudoscalar.real)

	def test_InvariantTerm_adjoint(self):
		SS1 = self.SCALAR_SINGLET.attr(symbol='ss1')
		SS2 = self.SCALAR_SINGLET.attr(symbol='ss2')
		SD1 = self.SCALAR_DOUBLET.attr(symbol='sd1').attr(hypercharge=1)
		SD2 = self.SCALAR_DOUBLET.attr(symbol='sd2').attr(hypercharge=-1)
		self.assertEqual(IT([SS1, SS2]).adjoint, IT([SS1, SS2]))
		self.assertEqual(IT([SD1, SD2]).adjoint.adjoint, IT([SD1, SD2]))
		self.assertEqual(
			IT([SD1, SD2], [SS1]).adjoint, IT([SD2.adjoint, SD1.adjoint], [SS1])
		)
		self.assertNotEqual(IT([SD1, SD2]).adjoint, IT([SD1, SD2]))

	def test_InvariantTerm_eq(self):
		H = STANDARD_MODEL.get_field('H')
		H_a = H.adjoint
		T1_1_A_0 = self.DATA['T1-1-A'].implement(0)
		φ, ϕ_ = T1_1_A_0.get_field('φ', "ϕ'")
		ϕ__a = ϕ_.adjoint
		ST1 = self.SCALAR_TRIPLET.attr(symbol='s1')
		ST2 = self.SCALAR_TRIPLET.attr(symbol='s2')
		ST3 = self.SCALAR_TRIPLET.attr(symbol='s3')
		ST4 = self.SCALAR_TRIPLET.attr(symbol='s4')
		# singlets
		self.assertEqual(IT([φ, φ, φ]), IT([φ], [φ, φ]))
		self.assertEqual(IT([φ, φ, φ]), IT([φ, φ], [φ]))
		self.assertEqual(IT([φ, φ, φ]), IT([φ], [φ], [φ]))
		self.assertNotEqual(IT([φ, φ, φ, φ]), IT([φ, φ]))
		# doublets
		self.assertEqual(IT([H, ϕ_], [φ, φ]), IT([ϕ_, H], [φ, φ]))
		self.assertEqual(IT([H, ϕ_], [φ, φ]), IT([φ, φ], [ϕ_, H]))
		self.assertEqual(IT([H, ϕ_], [H, ϕ_]), IT([H, ϕ_], [ϕ_, H]))
		self.assertEqual(IT([H, ϕ_], [H, ϕ_]), IT([ϕ_, H], [H, ϕ_]))
		self.assertEqual(IT([H, ϕ_], [H, ϕ_]), IT([ϕ_, H], [ϕ_, H]))
		self.assertEqual(IT([H_a, ϕ__a], [H, ϕ_]), IT([ϕ__a, H_a], [H, ϕ_]))
		self.assertEqual(IT([H_a, ϕ__a], [H, ϕ_]), IT([H, ϕ_], [ϕ__a, H_a]))
		# triplets
		self.assertEqual(IT([ST1, ST2, ST3]), IT([ST2, ST3, ST1]))
		self.assertEqual(IT([ST1, ST2, ST3]), IT([ST3, ST1, ST2]))
		self.assertNotEqual(IT([ST1, ST2, ST3]), IT([ST3, ST2, ST1]))
		self.assertEqual(IT([ST1, ST2, ST3, ST4]), IT([ST2, ST3, ST4, ST1]))
		self.assertEqual(IT([ST1, ST2, ST3, ST4]), IT([ST3, ST4, ST1, ST2]))
		self.assertEqual(IT([ST1, ST2, ST3, ST4]), IT([ST4, ST1, ST2, ST3]))
		self.assertNotEqual(IT([ST1, ST2, ST3, ST4]), IT([ST1, ST3, ST2, ST4]))

	def test_InvariantTerm_hash(self):
		for model, L in self.lagrangians.items():
			for term in L:
				adjoint = term.adjoint
				if adjoint == term:
					self.assertEqual(hash(adjoint), hash(term),
						'{}: {} ≠ {}'.format(
							model.name, str(adjoint), str(term)
						) + str(term._counter)
					)

	# iter(InvariantTerm) should have a consistent order
	def test_InvariantTerm_iter(self):
		SD1 = self.SCALAR_DOUBLET.attr(symbol='sd1').attr(hypercharge=1)
		SD2 = self.SCALAR_DOUBLET.attr(symbol='sd2').attr(hypercharge=-1)
		term = IT([SD1.adjoint, SD1], [SD2.adjoint, SD2])
		self.assertEqual(tuple(term.adjoint), tuple(term))
		# check all model terms
		for model, L in self.lagrangians.items():
			for term in L:
				adjoint = term.adjoint
				if adjoint == term:
					self.assertEqual(tuple(adjoint), tuple(term),
						msg='{}: {} ≠ {}'.format(
							model.name, str(adjoint), str(term)
						)
					)

	def test_Model_is_valid(self):
		SS = self.SCALAR_SINGLET
		SD = self.SCALAR_DOUBLET
		ST = self.SCALAR_TRIPLET
		FS = self.FERMION_SINGLET
		FD = self.FERMION_DOUBLET
		FT = self.FERMION_TRIPLET
		# using STANDARD_MODEL just to have a Model object (“dummy”)
		SM = STANDARD_MODEL
		self.assertFalse(SM.is_valid(
			[FS, FS.adjoint]
		))
		self.assertTrue(SM.is_valid(
			[SD, SD]
		))
		self.assertTrue(SM.is_valid(
			[ST, ST]
		))
		self.assertTrue(SM.is_valid(
			[FD, FD]
		))
		self.assertTrue(SM.is_valid(
			[FT, FT]
		))
		self.assertFalse(SM.is_valid(
			[SD.attr(hypercharge=2), SD.attr(hypercharge=2)]
		))
		self.assertTrue(SM.is_valid(
			[SD, SD, SS, SS]
		))
		self.assertTrue(SM.is_valid(
			[SD, ST, SD, SS]
		))
		self.assertFalse(SM.is_valid(
			[SD, ST, SD, SD]
		))
		self.assertTrue(SM.is_valid(
			[ST, ST, ST, SS]
		))
		self.assertTrue(SM.is_valid(
			[SD, ST, ST, SD]
		))
		self.assertTrue(SM.is_valid(
			[ST, ST, ST, ST]
		))
		self.assertFalse(SM.is_valid(
			[ST, ST, FS]
		))
		self.assertTrue(SM.is_valid(
			[ST, FT, FS]
		))
		self.assertTrue(SM.is_valid(
			[SS, FS, FS]
		))
		self.assertFalse(SM.is_valid(
			[SS.attr(z2=-1), FS.attr(z2=-1), FS.attr(z2=-1)]
		))

	def test_BSMModel_fields_without_anomalies(self):
		model = BSMModel('test', (
			FermionField('F1', 2, Y= 2),
			FermionField('F2', 2, Y=-2),
			FermionField('F3', 1, Y= 1),
		))
		self.assertEqual(
			len(model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]), 1
		)
		self.assertIn(
			model.get_field('F3', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		self.assertNotIn(Anomalies.WITTEN_ANOMALY, model.anomalies)
		model = BSMModel('test', (
			FermionField('F1', 2, Y= 2),
			FermionField('F2', 2, Y=-2),
			FermionField('F3', 2, Y= 0),
		))
		self.assertNotIn(Anomalies.GAUGE_ANOMALY_HYPERCHARGE, model.anomalies)
		self.assertEqual(len(model.anomalies[Anomalies.WITTEN_ANOMALY]), 1)
		self.assertIn(
			model.get_field('F3', original_fields=True),
			model.anomalies[Anomalies.WITTEN_ANOMALY]
		)
		# compare with arXiv:1308.3655
		model = self.DATA['T1-1-A'].implement(2)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-1-B'].implement(2)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-1-C'].implement(1)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-1-D'].implement(1)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-1-D'].implement(-1)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-1-F'].implement(1)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-1-G'].implement(2)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-1-H'].implement(2)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-2-A'].implement(0)
		self.assertIn(
			model.get_field("ψ'", original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-2-A'].implement(-2)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		self.assertIn(
			model.get_field("ψ'", original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-2-B'].implement(0)
		self.assertIn(
			model.get_field("ψ'", original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-2-B'].implement(-2)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		self.assertIn(
			model.get_field("ψ'", original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-2-D'].implement(1)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		self.assertIn(
			model.get_field("ψ'", original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-2-D'].implement(-1)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-2-F'].implement(1)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		self.assertIn(
			model.get_field("ψ'", original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-2-F'].implement(-1)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-3-A'].implement(0)
		self.assertFalse(model.anomalies)
		model = self.DATA['T1-3-B'].implement(0)
		self.assertFalse(model.anomalies)
		model = self.DATA['T1-3-C'].implement(1)
		self.assertIn(
			model.get_field('Ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		self.assertIn(
			model.get_field("ψ'", original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-3-D'].implement(1)
		self.assertIn(
			model.get_field('Ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		self.assertIn(
			model.get_field("ψ'", original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		# arXiv:1308.3655 claims that ψ must also be vector-like in this case,
		# but I don’t see why (and neither does the algorithm)
		self.assertNotIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		self.assertNotIn(Anomalies.WITTEN_ANOMALY, model.anomalies)
		model = self.DATA['T1-3-D'].implement(-1)
		self.assertIn(
			model.get_field('Ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		# arXiv:1308.3655 claims that ψ must also be vector-like in this case,
		# but I don’t see why (and neither does the algorithm)
		self.assertNotIn(
			model.get_field("ψ'", original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		self.assertNotIn(Anomalies.WITTEN_ANOMALY, model.anomalies)
		model = self.DATA['T1-3-F'].implement(1)
		self.assertIn(
			model.get_field('Ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		self.assertIn(
			model.get_field("ψ'", original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T1-3-G'].implement(0)
		self.assertFalse(model.anomalies)
		model = self.DATA['T3-A'].implement(0)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T3-A'].implement(-2)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T3-B'].implement(1)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)
		model = self.DATA['T3-C'].implement(1)
		self.assertIn(
			model.get_field('ψ', original_fields=True),
			model.anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
		)

	def test_trace(self):
		T1 = ScalarField('T1', 3, Y=0, z2=1)
		T2 = ScalarField('T2', 3, Y=0, z2=1)
		T3 = ScalarField('T3', 3, Y=0, z2=1)
		T4 = ScalarField('T4', 3, Y=0, z2=1)
		# trilinear
		self.assertEqual(IT([T1, T2, T3]), IT([T2, T3, T1]))
		self.assertEqual(IT([T1, T2, T3]), IT([T3, T1, T2]))
		self.assertNotEqual(IT([T1, T2, T3]), IT([T2, T1, T3]))
		self.assertEqual(IT([T2, T1, T3]), IT([T1, T3, T2]))
		self.assertEqual(IT([T2, T1, T3]), IT([T3, T2, T1]))
		# quartic
		self.assertEqual(IT([T1, T2, T3, T4]), IT([T2, T3, T4, T1]))
		self.assertEqual(IT([T1, T2, T3, T4]), IT([T3, T4, T1, T2]))
		self.assertEqual(IT([T1, T2, T3, T4]), IT([T4, T1, T2, T3]))
		self.assertNotEqual(IT([T1, T2, T3, T4]), IT([T2, T1, T3, T4]))
		self.assertEqual(IT([T2, T1, T3, T4]), IT([T1, T3, T4, T2]))
		self.assertEqual(IT([T2, T1, T3, T4]), IT([T3, T4, T2, T1]))
		self.assertEqual(IT([T2, T1, T3, T4]), IT([T4, T2, T1, T3]))
		self.assertNotEqual(IT([T1, T2, T3, T4]), IT([T2, T1, T4, T3]))
		self.assertNotEqual(IT([T2, T1, T3, T4]), IT([T2, T1, T4, T3]))
		self.assertEqual(IT([T2, T1, T4, T3]), IT([T1, T4, T3, T2]))
		self.assertEqual(IT([T2, T1, T4, T3]), IT([T4, T3, T2, T1]))
		self.assertEqual(IT([T2, T1, T4, T3]), IT([T3, T2, T1, T4]))

	# Test identities (see arXiv:2003.08037)
	def test_identities(self):
		model_fields = (
			ScalarField('S',  1, Y= 0,  z2=1),
			ScalarField('D',  2, Y= 0,  z2=1),
			ScalarField('T1', 3, Y= 0,  z2=1),
			ScalarField('T2', 3, Y= 0,  z2=1),
			ScalarField('T3', 3, Y= 0,  z2=1),
			ScalarField('TC', 3, Y= 70, z2=1),
		)
		doublets_normal = (
			ScalarField('D1', 2, Y= 30, z2=1),
			ScalarField('D2', 2, Y= 50, z2=1),
		)
		doublets_m = (
			ScalarField('D1', 2, Y= 1, z2=1),
			ScalarField('D2', 2, Y= 1, z2=1),
		)
		model = BSMModel('test', model_fields + doublets_normal)
		model_m = BSMModel('test_m', model_fields + doublets_m)
		H, S, D, D1, D2, T1, T2, T3, TC = model.get_field(
			'H', 'S', 'D', 'D1', 'D2', 'T1', 'T2', 'T3', 'TC'
		)
		D1m, D2m = doublets_m
		LL = model.lagrangian()
		LLm = model_m.lagrangian()
		### identity 1
		for term in LL:
			self.assertNotIn(IP(D, D), term)
		### identity 2
		doublet_quartics_D12 = []
		doublet_quartics_D = []
		doublet_quartics_H = []
		for term in LL:
			if (
				len(term) == 2 and len(term[0]) == len(term[1]) == 2 and
				all(f.su2_doublet for f in term.fields)
			):
				# terms with H, D1 and D2
				if D not in term.get_fields(original=True):
					doublet_quartics_D12.append(term)
				# terms with D only
				if all(f == D for f in term.get_fields(original=True)):
					doublet_quartics_D.append(term)
				# terms with H only
				if all(f == H for f in term.get_fields(original=True)):
					doublet_quartics_H.append(term)
		for doub in H, D1, D2:
			# 2 for mixed terms and 1 each for terms with all fields equal
			# (except for pure Higgs term)
			self.assertEqual(
				len([
					t for t in doublet_quartics_D12
					if doub not in t.get_fields(original=True)
				]), 4 if doub == H else 3
			)
		# total: 3×2 + 2 = 8 terms
		self.assertEqual(len(doublet_quartics_D12), 8)
		self.assertEqual(len(doublet_quartics_D), 1)
		# SM-only terms are omitted
		self.assertEqual(len(doublet_quartics_H), 0)
		### identity 3
		dtd_terms_3 = []
		dtd_terms_4 = []
		for term in LL:
			if D in term.get_fields(original=True):
				continue
			if len(term[0]) == 3:
				prod = term[0]
			elif len(term) == 2 and len(term[1]) == 3:
				prod = term[1]
			else:
				continue
			if (
				prod[0].su2_doublet and prod[1].su2_triplet and
				prod[2].su2_doublet
			):
				if len(term.fields) == 3:
					dtd_terms_3.append(term)
				elif len(term.fields) == 4:
					dtd_terms_4.append(term)
				else:
					raise AssertionError
		for trip in T1, T2, T3:
			# {D1,D2,H}^† T {D1,D2,H} → 3
			self.assertEqual(
				len([t for t in dtd_terms_3 if trip in t.fields]), 3
			)
		self.assertEqual(len(dtd_terms_3), 9)
		for trip in T1, T2, T3:
			# {D1,D2,H}^† T {D1,D2,H} → 3
			self.assertEqual(
				len([t for t in dtd_terms_4 if trip in t.fields]), 3
			)
		self.assertEqual(len(dtd_terms_4), 9)
		### identity 4
		triple_traces_tc = []
		triple_traces_no_tc = []
		for term in LL:
			for prod in term:
				if (
					len(prod) == 3 and all(f.su2_triplet for f in prod)
				):
					if TC in term.fields:
						triple_traces_tc.append(term)
					else:
						triple_traces_no_tc.append(term)
					break
		for term in triple_traces_no_tc:
			for trip1, trip2, trip3 in itertools.product(
				[T1, T2, T3], repeat=3
			):
				if trip1 == trip2 or trip2 == trip3 or trip1 == trip3:
					self.assertNotIn(IP(trip1, trip2, trip3), term)
		self.assertEqual(
			len([t for t in triple_traces_no_tc if len(t.fields) == 3]), 1
		)
		self.assertEqual(
			len([t for t in triple_traces_no_tc if len(t.fields) == 4]), 1
		)
		self.assertEqual(len(triple_traces_no_tc), 2)
		# 3 terms each for trilinear & quartic, with one term each for T1, T2
		# and T3
		self.assertEqual(
			len([t for t in triple_traces_tc if len(t.fields) == 3]), 3
		)
		self.assertEqual(
			len([t for t in triple_traces_tc if len(t.fields) == 4]), 3
		)
		self.assertEqual(len(triple_traces_tc), 6)
		for term in triple_traces_tc:
			self.assertIn(TC, term.fields)
			self.assertIn(TC.adjoint, term.fields)
		### identity 5
		triplet_quartics = []
		for term in LL:
			if (
				len(term.fields) == 4 and
				all(f.su2_triplet for f in term.fields)
			):
				triplet_quartics.append(term)
		for trip_comb in itertools.combinations_with_replacement(
			[T1, T2, T3, TC, TC.adjoint], 4
		):
			trip_set = set(trip_comb)
			trip_set_no_tc = {f for f in trip_set if f.original_field != TC}
			matching_terms = [
				term for term in triplet_quartics
				if trip_set.issuperset(set(term.fields))
			]
			# filter out unpaired TC
			if sum(f.Y for f in trip_set) != 0:
				trip_set = trip_set_no_tc
			# terms without TC
			comb_2 = itertools.combinations_with_replacement(trip_set_no_tc, 2)
			num_terms = len(list(
				itertools.combinations_with_replacement(comb_2, 2)
			))
			# terms with TC
			if TC in trip_set:
				# (X TC) * (X TC†) + (TC† TC) * comb([X_i])
				# + 2: cf. corollary for single complex triplet
				num_terms += (
					len(trip_set_no_tc)**2 +
					len(list(itertools.combinations_with_replacement(
						trip_set_no_tc, 2)
					)) + 2
				)
			self.assertEqual(
				len(matching_terms), num_terms,
				msg=(trip_set, matching_terms)
			)
		# corollary for single complex triplet
		self.assertEqual(
			len([
				t for t in triplet_quartics
				if all(f.original_field == TC for f in t.fields)
			]), 2
		)
		# corollary for single real triplet
		for trip in T1, T2, T3:
			self.assertEqual(
				len([
					t for t in triplet_quartics
					if all(f == trip for f in t.fields)
				]), 1
			)
		# corollary for single complex triplet
		self.assertEqual(
			len([
				t for t in triplet_quartics
				if all(f == TC for f in t.get_fields(original=True))
			]), 2
		)
		### identities 6 & 7
		ddtt_terms_no_tc = []
		ddtt_terms_tc = []
		for term in LLm:
			if (
				len(term.fields) == 4 and
				sum(f.su2_doublet for f in term.fields) == 2 and
				sum(f.su2_triplet for f in term.fields) == 2 and
				D not in term.fields and H not in term.fields
			):
				if TC in term.fields:
					ddtt_terms_tc.append(term)
				else:
					ddtt_terms_no_tc.append(term)
		for doub1, doub2 in itertools.combinations_with_replacement(
			[D1m, D2m], 2
		):
			d_terms_no_tc = [
				t for t in ddtt_terms_no_tc if {
					f for f in t.get_fields(original=True, unique=True)
					if f.su2_doublet
				} == {doub1, doub2}
			]
			d_terms_tc = [
				t for t in ddtt_terms_tc if {
					f for f in t.get_fields(original=True, unique=True)
					if f.su2_doublet
				} == {doub1, doub2}
			]
			# T1², T2², T3², T1T2, T1T3, T2T3
			for trip1, trip2 in itertools.combinations_with_replacement(
				[T1, T2, T3], 2
			):
				dt_terms_no_tc = [
					t for t in d_terms_no_tc if {
						f for f in t.get_fields(original=True, unique=True)
						if f.su2_triplet
					} == {trip1, trip2}
				]
				count = 1
				if doub1 != doub2:
					count *= 2
				if trip1 != trip2:
					count *= 2
				self.assertEqual(
					len(dt_terms_no_tc), count, msg=dt_terms_no_tc
				)
			# total for the current doublet combination:
			#     doub1 == doub2: 3 + 6 = 9
			#         1 each for T1², T2², T3² and 2 each for T1T2, T1T3, T2T3
			#     doub1 != doub2: 6 + 12 = 18
			#         2 each for T1², T2², T3² and 4 each for T1T2, T1T3, T2T3
			factor = 1 if doub1 == doub2 else 2
			self.assertEqual(len(d_terms_no_tc), factor * 9, msg=d_terms_no_tc)
			self.assertEqual(len(d_terms_tc), factor * 2, msg=d_terms_tc)
		self.assertEqual(len(ddtt_terms_no_tc), 2 * (9 + 18))
		self.assertEqual(len(ddtt_terms_tc), 2 * (2 + 4))

	# Test the Lagrangian for the model T1-3-B with α = 0 as shown in
	# arXiv:1812.11133 (https://arxiv.org/abs/1812.11133v2)
	def test_t1_3_b_0(self):
		H, L = STANDARD_MODEL.get_field('H', 'L')
		T1_3_B_0 = self.DATA['T1-3-B'].implement(0)
		LL = T1_3_B_0.lagrangian()
		ϕ, Ψ, ψ, ψ_ = T1_3_B_0.get_field('ϕ', 'Ψ', 'ψ', "ψ'")
		# mass terms
		self.assertIn(IT([ϕ.adjoint, ϕ]), LL)
		self.assertIn(IT([Ψ, Ψ]), LL)
		self.assertIn(IT([Ψ.adjoint, Ψ.adjoint]), LL)
		self.assertIn(IT([ψ, ψ_]), LL)
		self.assertIn(IT([ψ.adjoint, ψ_.adjoint]), LL)
		# pure scalar interaction terms
		# 4 scalars
		self.assertIn(IT([H.adjoint, ϕ, ϕ, H]), LL)
		self.assertIn(IT([ϕ, ϕ], [ϕ, ϕ]), LL)
		# Yukawa terms
		self.assertIn(IT([H.adjoint, ψ_], [Ψ]), LL)
		self.assertIn(IT([H, ψ_.adjoint], [Ψ.adjoint]), LL)
		self.assertIn(IT([H, ψ], [Ψ]), LL)
		self.assertIn(IT([H.adjoint, ψ.adjoint], [Ψ.adjoint]), LL)
		self.assertIn(IT([L, ϕ, ψ_]), LL)
		self.assertIn(IT([L.adjoint, ϕ, ψ_.adjoint]), LL)
		# LL should contain 13 terms for T1-3-B (α = 0)
		self.assertEqual(len(LL), 13)

	# Test the Lagrangian for the model T1-1-A with α = 0 as shown in
	# arXiv:0908.3729 (https://arxiv.org/abs/0908.3729v2)
	def test_t1_1_a_0(self):
		H, L = STANDARD_MODEL.get_field('H', 'L')
		T1_1_A_0 = self.DATA['T1-1-A'].implement(0)
		T1_1_A_0.omit_equivalent_scalars()
		LL = T1_1_A_0.lagrangian()
		φ, ϕ_, ψ = T1_1_A_0.get_field('φ', "ϕ'", 'ψ')
		# mass terms
		self.assertIn(IT([ϕ_.adjoint, ϕ_]), LL)
		self.assertIn(IT([φ, φ]), LL)
		self.assertIn(IT([ψ, ψ]), LL)
		self.assertIn(IT([ψ.adjoint, ψ.adjoint]), LL)
		# pure scalar interaction terms
		# 3 scalars
		self.assertIn(IT([H, ϕ_], [φ]), LL)
		self.assertIn(IT([H.adjoint, ϕ_.adjoint], [φ]), LL)
		# 4 scalars
		self.assertIn(IT([H, ϕ_], [H, ϕ_]), LL)
		self.assertIn(IT([H.adjoint, ϕ_.adjoint], [H.adjoint, ϕ_.adjoint]), LL)
		self.assertIn(IT([H.adjoint, H], [ϕ_.adjoint, ϕ_]), LL)
		self.assertIn(IT([ϕ_.adjoint, ϕ_], [ϕ_.adjoint, ϕ_]), LL)
		self.assertIn(IT([H.adjoint, H], [φ, φ]), LL)
		self.assertIn(IT([ϕ_.adjoint, ϕ_], [φ, φ]), LL)
		self.assertIn(IT([φ, φ, φ, φ]), LL)
		# The terms
		# |H|² |ϕ'|² = (H^† H) (ϕ'^† ϕ'),
		# |H ϕ'|²    = (H^† ϕ'^†) (H ϕ') and
		# |H^† ϕ'|²  = (H^† ϕ') (ϕ'^† H),
		# are redundant with respect to the parameter space due to identity 2.
		# arXiv:0908.3729 makes the choice to discard |H^† ϕ'|², while
		# minimal-lagrangians discards |H ϕ'|² instead, so the resulting
		# Lagrangian differs from the paper in this respect. However, both are
		# completely equivalent.
		self.assertIn(IT([H.adjoint, ϕ_], [ϕ_.adjoint, H]), LL)
		self.assertNotIn(IT([H.adjoint, ϕ_.adjoint], [H, ϕ_]), LL)
		# Yukawa terms
		self.assertIn(IT([ϕ_.adjoint, L], [ψ]), LL)
		self.assertIn(IT([L.adjoint, ϕ_], [ψ.adjoint]), LL)
		# LL should contain 16 terms for T1-1-A (α = 0)
		self.assertEqual(len(LL), 16)

	# Test the Lagrangian for the Higgs triplet model, see e.g.
	# arXiv:1201.6287 (https://arxiv.org/abs/1201.6287v2)
	def test_higgs_triplet(self):
		H, L = STANDARD_MODEL.get_field('H', 'L')
		Higgs_triplet = self.DATA['Higgs-triplet']
		Δ = Higgs_triplet.get_field('Δ')
		LL = Higgs_triplet.lagrangian()
		# mass term
		self.assertIn(IT([Δ.adjoint, Δ]), LL)
		# 3 scalars
		self.assertIn(IT([H, Δ.adjoint, H]), LL)
		self.assertIn(IT([H.adjoint, Δ, H.adjoint]), LL)
		# 4 scalars
		# The terms
		# Tr(Δ^†² Δ²) = 1/2 Tr(Δ^†)² Tr(Δ)², Tr((Δ^† Δ)²) and Tr(Δ^† Δ)²
		# are redundant with respect to the parameter space due to identity 5.
		# arXiv:1201.6287 makes the choice to discard
		# Tr(Δ^†² Δ²) and Tr(Δ^†)² Tr(Δ)², while minimal-lagrangians discards
		# Tr(Δ^†² Δ²) and Tr((Δ^† Δ)²) instead, so the resulting Lagrangian
		# differs from the paper in this respect. However, both are completely
		# equivalent.
		self.assertNotIn(IT([Δ.adjoint, Δ.adjoint, Δ, Δ]), LL)
		self.assertNotIn(IT([Δ.adjoint, Δ, Δ.adjoint, Δ]), LL)
		self.assertIn(IT([Δ.adjoint, Δ], [Δ.adjoint, Δ]), LL)
		self.assertIn(IT([Δ.adjoint, Δ.adjoint], [Δ, Δ]), LL)
		# The terms H^† H Tr(Δ^† Δ), H^† Δ^† Δ H and H^† Δ Δ^† H are redundant
		# with respect to the parameter space due to identity 6.
		# arXiv:1201.6287 makes the choice to discard H^† Δ^† Δ H, while
		# minimal-lagrangians discards H^† H Tr(Δ^† Δ) instead, so the
		# resulting Lagrangian differs from the paper in this respect. However,
		# both are completely equivalent.
		self.assertNotIn(IT([H.adjoint, H], [Δ.adjoint, Δ]), LL)
		self.assertIn(IT([H.adjoint, Δ.adjoint, Δ, H]), LL)
		self.assertIn(IT([H.adjoint, Δ, Δ.adjoint, H]), LL)
		# Yukawa terms
		self.assertIn(IT([L, Δ, L]), LL)
		self.assertIn(IT([L.adjoint, Δ.adjoint, L.adjoint]), LL)
		# LL should contain 9 terms for the Higgs triplet model
		self.assertEqual(len(LL), 9)


	# Test the Lagrangians for the models from
	# arXiv:1311.5896 (https://arxiv.org/abs/1311.5896v1)
	def test_cheung_sanford(self):
		H, L = STANDARD_MODEL.get_field('H', 'L')
		# Model A: singlet–doublet fermion
		SDF = self.DATA['SDF']
		LL = SDF.lagrangian()
		S, D1, D2 = SDF.get_field('S', 'D_1', 'D_2')
		# mass terms
		self.assertIn(IT([S, S]), LL)
		self.assertIn(IT([S.adjoint, S.adjoint]), LL)
		self.assertIn(IT([D1, D2]), LL)
		self.assertIn(IT([D1.adjoint, D2.adjoint]), LL)
		# Yukawa terms
		self.assertIn(IT([H, D1], [S]), LL)
		self.assertIn(IT([H.adjoint, D1.adjoint], [S.adjoint]), LL)
		self.assertIn(IT([H.adjoint, D2], [S]), LL)
		self.assertIn(IT([H, D2.adjoint], [S.adjoint]), LL)
		# LL should contain 8 terms for the singlet–doublet fermion model
		self.assertEqual(len(LL), 8)
		# Model B: singlet–doublet scalar
		SDS = self.DATA['SDS']
		LL = SDS.lagrangian()
		S, D = SDS.get_field('S', 'D')
		# mass terms
		self.assertIn(IT([S, S]), LL)
		self.assertIn(IT([D.adjoint, D]), LL)
		# 3 scalars
		self.assertIn(IT([D.adjoint, H], [S]), LL)
		self.assertIn(IT([H.adjoint, D], [S]), LL)
		# 4 scalars
		self.assertIn(IT([H.adjoint, H], [S, S]), LL)
		self.assertIn(IT([D.adjoint, D], [H.adjoint, H]), LL)
		self.assertIn(IT([D.adjoint, H], [H.adjoint, D]), LL)
		self.assertIn(IT([D.adjoint, H], [D.adjoint, H]), LL)
		self.assertIn(IT([H.adjoint, D], [H.adjoint, D]), LL)
		# the paper omits DM self-interactions, which are included here
		self.assertIn(IT([D.adjoint, D], [D.adjoint, D]), LL)
		self.assertIn(IT([D.adjoint, D], [S, S]), LL)
		self.assertIn(IT([S, S, S, S]), LL)
		# The term |H D|² = (H^† D^†) (H D) is redundant with other terms
		# (|H^† D|² and |H|² |D|²) with respect to the parameter space due to
		# identity 2 and should thus not appear
		self.assertNotIn(IT([H.adjoint, D.adjoint], [H, D]), LL)
		# LL should contain 9 + 3 = 12 terms for the singlet–doublet
		# scalar model
		self.assertEqual(len(LL), 12)
		# Model C: singlet–triplet scalar
		STS = self.DATA['STS']
		LL = STS.lagrangian()
		S, T = STS.get_field('S', 'T')
		# mass terms
		self.assertIn(IT([S, S]), LL)
		self.assertIn(IT([T, T]), LL)
		# 4 scalars
		self.assertIn(IT([H.adjoint, H], [S, S]), LL)
		# The terms H^† H Tr(T²) and H^† T² H are redundant with respect to the
		# parameter space due to identity 6.
		# arXiv:1311.5896 makes the choice to discard H^† T² H, while
		# minimal-lagrangians discards H^† H Tr(T²) instead, so the resulting
		# Lagrangian differs from the paper in this respect. However, both are
		# completely equivalent.
		self.assertNotIn(IT([H.adjoint, H], [T, T]), LL)
		self.assertIn(IT([H.adjoint, T, T, H]), LL)
		self.assertIn(IT([H.adjoint, T, H], [S]), LL)
		# the paper omits DM self-interactions, which are included here
		self.assertIn(IT([T, T], [S, S]), LL)
		self.assertIn(IT([T, T], [T, T]), LL)
		self.assertIn(IT([S, S, S, S]), LL)
		# this term is zero unless there are at least 3 generations of T
		self.assertNotIn(IT([T, T, T], [S]), LL)
		# LL should contain 5 + 3 = 8 terms for the singlet–triplet scalar
		# model
		self.assertEqual(len(LL), 8)

if __name__ == '__main__':
	unittest.main()

