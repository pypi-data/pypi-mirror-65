import collections
import enum
import functools
import itertools
import operator
from fractions import Fraction
from . import fields
from . import terms
from . import unicode_util
from .fields import FermionField, ScalarField
from .terms import InvariantTerm, Lagrangian, TermTypes


@enum.unique
class TermStatus(enum.Enum):
	ACCEPTED = True
	DISCARDED = False
	ZERO = 'ZERO'

class DuplicateNameError(Exception): pass

class Model:
	def __init__(self, name, fields):
		self.name = name
		self.fields = fields = tuple(fields)
		self.u1_len = max(len(field.u1) for field in fields)
		self.check_duplicate_names()

	@property
	def components(self):
		return tuple(c for f in self.fields for c in f.components)

	@property
	def scalars(self):
		return tuple(f for f in self.fields if f.scalar)

	@property
	def fermions(self):
		return tuple(f for f in self.fields if f.fermion)

	def check_duplicate_names(self, formatter=None):
		seen_symbol = {}
		seen_sarah = {}
		seen_formatter = {}
		for f in self.fields:
			name = None
			symbol = False
			if f.symbol in seen_symbol:
				symbol = True
				name = f.symbol
				f_prev = seen_symbol[name]
			elif f.sarah_symbol in seen_sarah:
				name = f.sarah_symbol
				f_prev = seen_sarah[name]
			elif formatter and formatter.format_field(f) in seen_formatter:
				name = formatter.format_field(f)
				f_prev = seen_formatter[name]
			if name:
				if symbol:
					msg = 'Name {} in model {} is used multiple times!'.format(
						f.symbol, self.name
					)
				else:
					msg = (
						'Fields {} and {} in model {} lead to duplicate names'
						'when formatting ({})!'
					).format(f_prev.symbol, f.symbol, self.name, name)
				raise DuplicateNameError(msg)
			seen_symbol[f.symbol] = f
			if f.sarah_symbol: seen_sarah[f.sarah_symbol] = f
			if formatter: seen_formatter[formatter.format_field(f)] = f

	@property
	def witten_anomaly(self):
		# Check for Witten SU(2) anomaly
		fermion_doublets = [
			f for f in self.fields if f.bsm and f.fermion and f.su2_doublet
		]
		return len(fermion_doublets) % 2 != 0

	# returns a list with entries of the form
	#	- [[field1, field2, …]] (scalars or neutral fermions) or
	#	- [[pos_field1, pos_field2, …], [neg_field1, neg_field2, …]]
	#		(charged fermions)
	def ewsb_mixing_fields(self, cpv=True):
		if cpv:
			def mix_key(comp): return comp.quantum_numbers
		# if no CP violation: prevent mixing between scalars and pseudoscalars
		else:
			neutral_scalars = {
				c.complex_parts.scalar
				for f in self.fields for c in f.components
				if c.scalar and c.neutral
			}
			neutral_pseudoscalars = {
				c.complex_parts.pseudoscalar
				for f in self.fields for c in f.components
				if c.scalar and c.neutral
			}
			def mix_key(comp):
				if comp in neutral_scalars: prop = 'S'
				elif comp in neutral_pseudoscalars: prop = 'P'
				else: prop = 'X'
				return comp.quantum_numbers + (prop,)
		components = set()
		# exclude quarks from mixing
		for orig_f in (f for f in self.fields if f.su3 == 0):
			fields = [orig_f, orig_f.adjoint] if orig_f.scalar else [orig_f]
			for field in fields:
				for multiplet_components in field.components:
					for c in multiplet_components.components:
						components.add(c)
		components = sorted(
			components, key=lambda c: mix_key(c) + (c.symbol,)
		)
		mixing_groups = [
			list(g) for _, g in itertools.groupby(components, key=mix_key)
		]
		# create set of neutral scalar/pseudoscalar pairs
		neutral_scalars_parts = {
			frozenset(c.complex_parts)
			for f in self.fields for c in f.components
			if c.scalar and c.neutral
		}
		# Mixing_groups now contains all mixed fields *and* (for scalars) their
		# adjoints.
		# For scalars: pick only one of the two options for each mixed field.
		# For charged fermions: combine positively- and negatively-charged
		# pairs.
		# Note: There could be a problem here with odd numbers of fermions with
		# matching charges (so they cannot all be matched up in pairs as Dirac
		# fermions and one charged fermion will be massless), but gauge
		# anomalies ensure that such field contents cannot occur.
		groups_unique = {}
		neutral_scalars_nomix = []
		for group in mixing_groups:
			field0 = group[0]
			key = mix_key(field0)
			key_adj = mix_key(field0.adjoint)
			if field0.scalar:
				if (
					key_adj not in groups_unique or (
						# pick the option with fewer conjugate fields
						key_adj in groups_unique and
							sum(f.is_adjoint for f in group) <
							sum(
								f.is_adjoint for f in groups_unique[key_adj][0]
							)
					)
				):
					groups_unique.pop(key_adj, None)
					# if the group only contains a single scalar/pseudoscalar
					# pair, then there will be no mixing
					if (
						len(group) == 2 and
						frozenset(group) in neutral_scalars_parts
					):
						# special case for Higgs boson: omit un-mixed Ah
						H0 = STANDARD_MODEL.get_field('H').components[1]
						if set(group) == set(H0.complex_parts):
							neutral_scalars_nomix.append(
								H0.complex_parts.scalar
							)
						else:
							neutral_scalars_nomix += group
					# else: add group normally
					else:
						groups_unique[key] = [group]
			elif field0.fermion:
				if key_adj not in groups_unique or field0.neutral:
					groups_unique[key] = [group]
				else:
					groups_unique[key_adj] = [group] + groups_unique[key_adj]
			else: assert False
		result = (
			list(groups_unique.values()) +
			[[[g]] for g in neutral_scalars_nomix]
		)
		return result

	def ewsb_mixed_fields(self, cpv=True):
		H = STANDARD_MODEL.get_field('H')
		mixing_groups = self.ewsb_mixing_fields(cpv=cpv)
		result = []
		for key, groups in itertools.groupby(
			mixing_groups,
			key=lambda mg_group: (mg_group[0][0].type, mg_group[0][0].charge)
		):
			lg = list(groups)
			# keep track of some lists to enable nicer naming
			trivials = [
				sum(
					f.generations for mix_group in sf_mix_groups
					for f in mix_group
				) == len(sf_mix_groups)
				for sf_mix_groups in lg
			]
			sm_fields = [
				any(
					not f.bsm for mix_group in sf_mix_groups
					for f in mix_group
				)
				for sf_mix_groups in lg
			]
			# process collection of same Lorentz type and charge
			charge_idx = 1
			result_add = []
			assert len(trivials) == len(sm_fields) == len(lg)
			for sf_mix_groups, trivial, sm_field in zip(
				lg, trivials, sm_fields
			):
				update_charge_idx = False
				mix_group_entry = []
				for mix_group in sf_mix_groups:
					if len(lg) == 1 or (
						(sum(trivials) == len(lg) - 1 and not trivial) or
						(sum(sm_fields) == len(lg) - 1 and not sm_field)
					):
						suffix = ''
					else:
						suffix = unicode_util.int_to_scripts(
							charge_idx, unicode_util.SUBSCRIPTS
						)
						update_charge_idx = True
					mix_group_entry.append(
						fields.MixedField(mix_group, symbol_suffix=suffix)
					)
				charge_idx += update_charge_idx
				if mix_group_entry:
					result_add.append(mix_group_entry)
			result += result_add
		# sort SM fields first
		result.sort(
			key=lambda mix_group: any(
				not f.bsm for fm in mix_group for f in fm.gauge_es
			), reverse=True
		)
		return result

	def ewsb_dirac_spinors(self):
		mixed_fermions = [
			mix_group for mix_group in self.ewsb_mixed_fields()
			if mix_group[0].fermion
		]
		non_mixing_fields = {
			c
			for multiplet in self.fields
			for multiplet_comp in multiplet.components
			for c in multiplet_comp.components
			# exclude quarks from mixing
			if multiplet.su3 == 0
		} - {
			f for group in mixed_fermions for mf in group for f in mf.gauge_es
		}
		result = []
		for mix_group in mixed_fermions:
			assert len(mix_group) in (1, 2)
			f_pos = mix_group[0]
			if len(mix_group) == 1:
				f_neg = f_pos
			else:
				f_neg = mix_group[1]
			assert f_pos.charge == f_neg.adjoint.charge
			assert f_pos.u1 == f_neg.adjoint.u1
			assert len(f_pos.gauge_es) == len(f_neg.gauge_es)
			result.append(fields.DiracFermionField(f_pos, f_neg.adjoint))
		for f in non_mixing_fields:
			if f.fermion:
				result.append(fields.DiracFermionField(f, 0))
		# sort SM fields first
		result.sort(
			key=lambda fd: any(
				not weyl.bsm
				for weyl in fd.left.gauge_es + (
					fd.right.gauge_es if isinstance(fd.right, fields.Field)
						else ()
				)
			), reverse=True
		)
		return result

	def get_field(self, *symbols, original_fields=False):
		fields = self.original_fields if original_fields else self.fields
		result = [field for symbol in symbols for field in fields
			if symbol == field.symbol]
		if len(result) != len(symbols):
			raise ValueError('Field(s) not found: {}'.format(symbols))
		if len(result) == 1:
			return result[0]
		else:
			return result

	def term_from_symbols(self, *parts):
		return tuple(tuple(self.get_field(symbol) for symbol in tup)
			for tup in parts)

	def is_valid(self, term_comb):
		# renormalizability
		if not TermTypes.from_term_comb(term_comb, no_exception=True):
			return False
		# Lorentz invariance: must have an even number of left- and
		# right-handed Weyl spinors
		weyl_num_l = sum(f.fermion and not f.is_adjoint for f in term_comb)
		weyl_num_r = sum(f.fermion and f.is_adjoint for f in term_comb)
		lorentz_scalar = (weyl_num_l % 2 == 0) and (weyl_num_r % 2 == 0)
		# SU(3) invariance (only for quarks)
		su3_scalar = sum(f.su3 for f in term_comb) == 0
		# gauge invariance: SU(2), U(1), ℤ₂
		su2_scalar = sum(f.su2_multiplicity - 1 for f in term_comb) % 2 == 0
		y_total = sum(f.hypercharge for f in term_comb)
		z2_total = functools.reduce(operator.mul, [f.z2 for f in term_comb], 1)
		u1_totals = [
			sum(f.u1[i] if i < len(f.u1) else 0 for f in term_comb)
			for i in range(self.u1_len)
		]
		return (
			lorentz_scalar and su3_scalar and su2_scalar and y_total == 0 and
			z2_total == 1 and all(q == 0 for q in u1_totals)
		)

	@staticmethod
	# returns a list of InvariantTerms
	def generate_terms(term_comb):
		assert len(term_comb) <= 4
		term_type = TermTypes.from_term_comb(term_comb)
		singlets = tuple(sorted([f for f in term_comb if f.su2_singlet],
			key=lambda f: not f.is_adjoint))
		doublets = tuple(sorted([f for f in term_comb if f.su2_doublet],
			key=lambda f: not f.is_adjoint))
		triplets = tuple(sorted([f for f in term_comb if f.su2_triplet],
			key=lambda f: not f.is_adjoint))
		# 1 triplet and 1–3 singlets: terms like this are always 0!
		if len(triplets) == 1 and not doublets:
			return []
		if term_type in (TermTypes.S3, TermTypes.S4, TermTypes.YUKAWA):
			# 3 or 4 singlets
			if len(singlets) == len(term_comb):
				return [InvariantTerm(singlets)]
			# 4 doublets (must all be scalars)
			if len(doublets) == len(term_comb) == 4:
				# use sets to get unique permutations
				perms = [
					InvariantTerm(perm[:2], perm[2:])
					for perm in set(itertools.permutations(doublets))
				]
				return perms
			# 2–4 triplets, any number of singlets
			elif triplets and not doublets:
				# use set to get unique permutations
				# cosmetic: use reversed to produce permutations in sorted
				# order, in order to get (and keep) Tr(T1 T2 T3) first instead
				# of Tr(T2 T3 T1)
				perms = [
					InvariantTerm(reversed(perm), singlets)
					for perm in set(itertools.permutations(triplets))
				]
				# two traces of two triplets each (must all be scalars)
				if len(triplets) == len(term_comb) == 4:
					assert not singlets
					perms += [
						InvariantTerm(perm[:2], perm[2:])
						for perm in set(itertools.permutations(triplets))
					]
				return perms
			# 2 doublets and 1 or 2 singlets
			if len(doublets) == 2 and not triplets:
				return [InvariantTerm(doublets, singlets)]
			# 2 doublets and (1 triplet and ≤1 singlet) or (2 triplets)
			elif len(doublets) == 2 and triplets:
				# [(D_1, D_2), (D_2, D_1)]
				doublet_perms = itertools.permutations(doublets)
				# [(T,)] or [(T_1, T_2), (T_2, T_1)]
				triplet_perms = itertools.permutations(triplets)
				# [((D_1, D_2), (T,)), ((D_2, D_1), (T,))] or
				# [((D_1, D_2), (T_1, T_2)), ((D_1, D_2), (T_2, T_1)),
				#  ((D_2, D_1), (T_1, T_2)), ((D_2, D_1), (T_2, T_1))]
				# use set to get unique permutations
				candidates = set(itertools.product(
					doublet_perms, triplet_perms
				))
				# terms of the form D T D or D T² D
				terms = [
					InvariantTerm(
						(cand[0][0],) + cand[1] + (cand[0][1],), singlets
					)
					for cand in candidates
				]
				# terms of the form D² Tr(T²) (must all be scalars)
				if len(triplets) == 2:
					assert not singlets
					terms += [
						InvariantTerm(cand[0], cand[1]) for cand in candidates
					]
				return terms
			# only remaining combinations:
			# (3 doublets, ≤1 triplet) and (1 doublet, 3 triplets) are not
			# possible
			else:
				raise ValueError(
					'Invalid term combination: {}'.format(term_comb)
				)
		# mass terms
		else:
			return [InvariantTerm(term_comb)]

	@staticmethod
	def filter_terms_identities(term):
		### identity 1
		for prod in term:
			if (
				len(prod) == 2 and prod[0] == prod[1] and
				all(f.scalar and f.su2_doublet for f in prod)
			):
				return TermStatus.ZERO
		# other mass terms are always OK
		if term.term_type.mass_term:
			return TermStatus.ACCEPTED
		### identity 2
		if (
			len(term) == 2 and len(term[0]) == len(term[1]) == 2 and
			len(term.fields) == sum(f.su2_doublet for f in term.fields)
		):
			unique = term.get_fields(original=True, unique=True, sort=True)
			# D₁ = D₂: automatically fulfilled since |D D|² is excluded by
			#          identity 1
			# D₁ ≠ D₂: use variants |D₁^† D₂|² and |D₁|² |D₂|²
			#          (exclude |D₁D₂|²)
			if len(unique) == 2:
				D1, D2 = unique
				return TermStatus(
					term != InvariantTerm([D1.adjoint, D2.adjoint], [D1, D2])
				)
		### identity 3
		if len(term[0]) == 3:
			prod = term[0]
		elif len(term) == 2 and len(term[1]) == 3:
			prod = term[1]
		if prod[0].su2_doublet and prod[1].su2_triplet and prod[2].su2_doublet:
			D1, D2 = [f for f in prod.get_fields(sort=True) if f.su2_doublet]
			T = prod[1]
			prod_adjnum = sum(f.is_adjoint for f in prod)
			adj_adjnum = sum(f.is_adjoint for f in prod.adjoint)
			assert prod_adjnum > 0 or adj_adjnum > 0
			if D1 == D2:
				result = TermStatus.ACCEPTED
			else:
				assert len(term) <= 2
				rest = ()
				if len(term) == 2:
					rest = term[0] if term[1] == prod else term[1]
				swapped = InvariantTerm([D2, T, D1], rest).to_tuples()
				term = term.to_tuples()
				# taking the adjoint flips the order of terms, so for the case
				# of the terms {D₁ T D₂, D₂ T D₁, D₁^† T D₂^†, D₂^† T D₁^†}, we
				# want to keep (D₁ T D₂ + H.c.) since this is lexically <
				# (D₂ T D₁ + H.c.).
				# When checking D₁ T D₂ and D₂ T D₁:
				#   D1 = D₁, D2 = D₂, swapped = D₂ T D₁, so term != swapped
				# When checking D₁^† T D₂^†, D₂^† T D₁^†:
				#   D1 = D₁^†, D2 = D₂^†, swapped = D₂^† T D₁^†,
				#   so term == swapped
				result = TermStatus(
					(prod_adjnum <= adj_adjnum and term != swapped) or
					(prod_adjnum > adj_adjnum and term == swapped)
				)
			return result
		### identity 4
		for prod in term:
			if len(prod) == 3 and all(f.su2_triplet for f in prod):
				assert len(term) <= 2
				p_fields = prod.get_fields(unique=True, sort=True)
				if len(p_fields) < len(prod):
					return TermStatus.ZERO
				else:
					rest = ()
					if len(term) == 2:
						rest = term[0] if term[1] == prod else term[1]
					return TermStatus(term == InvariantTerm(p_fields, rest))
		### identity 5
		if (
			len(term.fields) == 4 and len(term) == 1 and
			all(f.su2_triplet for f in term.fields)
		):
			return TermStatus.DISCARDED
		### identities 6 & 7
		if (
			len(term.fields) == 4 and
			sum(f.su2_doublet for f in term.fields) == 2 and
			sum(f.su2_triplet for f in term.fields) == 2
		):
			D1, D2 = [f for f in term.get_fields(sort=True) if f.su2_doublet]
			T1, T2 = [f for f in term.get_fields(sort=True) if f.su2_triplet]
			# general case: use variants D₁^† T₁ T₂ D₂ and D₁^† T₂ T₁ D₂
			# (exclude D₁^† D₂ Tr(T₁ T₂))
			cond = (
				term != InvariantTerm([D1, D2], [T1, T2]) and
				# identity 8: doublets do not have to be swapped
				term != InvariantTerm([D2, T1, T2, D1]) and
				term != InvariantTerm([D2, T2, T1, D1])
			)
			# if D₁ = D₂ = D, then D² Tr(T₁ T₂) = 0 and only one of the two
			# terms should be kept
			if D1 == D2:
				cond = cond and (term != InvariantTerm([D1, T2, T1, D2]))
			return TermStatus(cond)
		# trace equality due to cyclic permutations is checked in __eq__
		return TermStatus.ACCEPTED


STANDARD_MODEL = Model('Standard Model', (
	ScalarField ('H',     2, Y= 1,               z2=1),
	FermionField('L',     2, Y=-1,               z2=1),
	FermionField('Q',     2, Y=Fraction(' 1/3'), z2=1),
	FermionField('e_R^c', 1, Y= 2,               z2=1),
	FermionField('u_R^c', 1, Y=Fraction('-4/3'), z2=1),
	FermionField('d_R^c', 1, Y=Fraction(' 2/3'), z2=1),
))
# set additional attributes on Standard Model fields
def _():
	L, eRc, H = STANDARD_MODEL.get_field('L', 'e_R^c', 'H')
	Q, uRc, dRc = STANDARD_MODEL.get_field('Q', 'u_R^c', 'd_R^c')
	# set SU(3) representations for quarks
	Q.su3 = 3
	uRc.su3 = -3
	dRc.su3 = -3
	# set number of generations
	for f in STANDARD_MODEL.fields:
		if f != STANDARD_MODEL.get_field('H'):
			f.generations = 3
	# add special names for Standard Model fields in SARAH output
	L.sarah_symbol = 'l'
	L.sarah_component_symbols = ('vL', 'eL')
	L.sarah_mixing_symbols = (('VL', 'Uneu'), ('EL', 'Ve'))
	L.sarah_dirac_spinor_symbols = ('Fv', 'Fe')
	L.sarah_charge_preference = '-'
	eRc.sarah_symbol = 'e'
	eRc.sarah_component_symbols = ('conj[eR]',)
	eRc.sarah_mixing_symbols = (('ER', 'Ue'),)
	eRc.sarah_dirac_spinor_symbols = ('Fe',)
	eRc.sarah_charge_preference = '-'
	H.sarah_component_symbols = ('Hp', 'H0')
	H.sarah_vev_symbols = ('v', 'Ah', 'hh')
	Q.sarah_symbol = 'q'
	Q.sarah_component_symbols = ('uL', 'dL')
	Q.sarah_mixing_symbols = (('UL', 'Vu'), ('DL', 'Vd'))
	uRc.sarah_symbol = 'u'
	uRc.sarah_component_symbols = ('conj[uR]',)
	uRc.sarah_mixing_symbols = (('UR', 'Uu'),)
	dRc.sarah_symbol = 'd'
	dRc.sarah_component_symbols = ('conj[dR]',)
	dRc.sarah_mixing_symbols = (('DR', 'Ud'),)
_()
del _

@enum.unique
class Anomalies(enum.Enum):
	GAUGE_ANOMALY_HYPERCHARGE = 'GAUGE_ANOMALY_HYPERCHARGE'
	WITTEN_ANOMALY = 'WITTEN_ANOMALY'

class BSMModel(Model):
	def __init__(self, name, fields, param_values=()):
		fields = tuple(f.attr(bsm=True) for f in fields)
		super().__init__(name, STANDARD_MODEL.fields + fields)
		for field in fields:
			assert len(field.u1) == self.u1_len, \
				'All fields must have the same number of global U(1) charges!'
		self.original_fields = self.fields
		self.param_values = tuple(param_values)
		self.original_name = name
		self.imp_param_value = None
		self.anomalies = {}
		if not param_values:
			self.anomalies = self.fields_without_anomalies()

	def omit_equivalent_scalars(self):
		len_fields = len(self.fields)
		# remove scalar fields which are equivalent to others
		sm_fields = [f for f in self.fields if not f.bsm]
		filtered_fields = []
		for candidate in self.fields:
			if candidate.bsm and (
				candidate.fermion or not any(chosen.is_equivalent(candidate)
					for chosen in filtered_fields
				)
			):
				filtered_fields.append(candidate)
		self.fields = tuple(sm_fields + filtered_fields)
		assert len(self.fields) <= len_fields

	def fields_without_anomalies(self):
		len_fields = len(self.fields)
		# check if fermions need to be made vector-like to cancel anomalies
		sm_fields = [f for f in self.fields if not f.bsm]
		bsm_fields  = [f for f in self.fields if f.bsm]
		scalars = [f for f in bsm_fields if f.scalar]
		fermions_neutral = [f for f in bsm_fields if f.fermion and f.Y == 0]
		fermions_charged = [f for f in bsm_fields if f.fermion and f.Y != 0]
		anomalies = {}
		vectorlike_fermions = []
		vectorlike_doublet = []
		# Cancel gauge anomalies:
		# Find fermions which are not paired with an opposite-hypercharge
		# counterpart and make them vector-like.
		charges = collections.Counter(
			(f.su2_multiplicity, f.Y) for f in fermions_charged
		)
		paired = set()
		for f in fermions_charged:
			if charges[(f.su2_multiplicity, -f.Y)] > 0:
				charges[(f.su2_multiplicity, -f.Y)] -= 1
				paired.add(f)
		unpaired = set(fermions_charged) - paired
		if unpaired:
			vectorlike_fermions = [
				weyl_fermion.original_field
				for f in unpaired
				for weyl_fermion in fields.VectorLikeFermionField.from_field(
					f, bsm=True
				)
			]
			anomalies[Anomalies.GAUGE_ANOMALY_HYPERCHARGE] = unpaired
		self.fields = tuple(
			sm_fields + scalars + fermions_neutral + list(paired) +
			vectorlike_fermions + vectorlike_doublet
		)
		# Cancel Witten SU(2) anomaly:
		# The number of fermion doublets must be even. Since charged fermion
		# doublets were already paired in the previous step, the number of
		# hypercharged-neutral fermion doublets must be odd. Pick any of these
		# doublets and make it vector-like.
		if self.witten_anomaly:
			neutral_doublets = [f for f in fermions_neutral if f.su2_doublet]
			assert neutral_doublets
			d = neutral_doublets[0]
			fermions_neutral = [f for f in fermions_neutral if f != d]
			vectorlike_doublet = [
				weyl_fermion.original_field for weyl_fermion in
				fields.VectorLikeFermionField.from_field(d, bsm=True)
			]
			anomalies[Anomalies.WITTEN_ANOMALY] = {d}
			self.fields = tuple(
				sm_fields + scalars + fermions_neutral + list(paired) +
				vectorlike_fermions + vectorlike_doublet
			)
		assert len(self.fields) >= len_fields
		assert not self.witten_anomaly
		self.check_duplicate_names()
		return anomalies

	def implement(self, alpha):
		nop = alpha == 0 and not self.param_values
		assert nop or alpha in self.param_values
		if nop:
			return self
		# add α to hypercharges
		imp_fields = tuple(f.attr(hypercharge=f.Y + alpha)
			for f in self.fields if f.bsm)
		# create and return result object
		alpha_str = str(alpha).replace('-', '−')
		result = BSMModel(
			'{} (α = {})'.format(self.name, alpha_str), imp_fields
		)
		result.original_name = self.name
		result.imp_param_value = alpha
		return result

	def lagrangian(self, omit_sm=True):
		scalars = tuple(s.adjoint for s in self.scalars
			if s.adjoint != s) + self.scalars
		fermions = tuple(f.adjoint for f in self.fermions
			if f.adjoint != f) + self.fermions
		all_fields = scalars + fermions
		term_combs = []
		for num_total in range(2, terms.MASS_DIMENSION_MAX + 1):
			candidates = itertools.combinations_with_replacement(
				all_fields, num_total
			)
			term_combs += [
				term_comb for term_comb in candidates
				if self.is_valid(term_comb)
			]
		# exclude pure Standard Model terms
		if omit_sm:
			term_combs = [
				comb for comb in term_combs
				if any(f.bsm for f in comb)
			]
		# generate proper terms from field combinations
		all_terms = [
			term for comb in term_combs for term in self.generate_terms(comb)
		]
		accepted_terms = []
		discarded_terms = []
		for term in all_terms:
			status = self.filter_terms_identities(term)
			if status == TermStatus.ACCEPTED:
				accepted_terms.append(term)
			elif status == TermStatus.DISCARDED:
				discarded_terms.append(term)
		# add terms which will be discarded from the set due to == equality to
		# discarded_terms
		discarded_terms += [
			f for f, count in collections.Counter(accepted_terms).items()
			if count > 1
		]
		L = Lagrangian(accepted_terms, discarded_terms=discarded_terms)
		return L

