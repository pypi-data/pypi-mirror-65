import collections
import copy
from fractions import Fraction
from . import unicode_util
from .output import plain as output_plain


REAL_PART_SUFFIX = 'Re'
IMAG_PART_SUFFIX = 'Im'
MIX_FERMION_NAME = 'fmx'
MIX_SCALAR_NAME = 'smx'


# type: 'S' or 'F' for scalar or (Weyl) fermion
#       Note that Weyl fermions are always assumed to be left-handed, i.e. in
#       the (½, 0) representation of SL(2, ℂ)
# su2_multiplicity: what representation of SU(2) the field is in (singlet,
#	doublet, triplet). Note that triplets are assumed to be in the adjoint
#	representation (“matrix form”).
# Y: value of the field’s hypercharge Y
# z2: value of the discrete ℤ₂ symmetry of the Lagrangian (1 or -1)
# u1: charges of global U(1) symmetries of the Lagrangian
class Field:
	@staticmethod
	def from_field(field):
		return copy.copy(field)

	_repr_str = (
		'{}({!r}, {!r}, {!r}, Y={!r}, z2={!r}, u1={!r}, is_adjoint={!r})'
	)

	def __init__(
		self, symbol, lorentz_type, su2_multiplicity, Y, z2=-1, u1=(),
		is_adjoint=False
	):
		self.symbol = symbol
		self.type = lorentz_type
		self.su3 = 0
		self.su2_multiplicity = su2_multiplicity
		self.hypercharge = Y
		self.z2 = z2
		self.u1 = tuple(u1)
		self.is_adjoint = is_adjoint
		self.bsm = False
		self.generations = 1
		self.sarah_symbol = None
		self.sarah_component_symbols = None
		self.sarah_vev_symbols = None
		self.sarah_mixing_symbols = None
		self.sarah_dirac_spinor_symbols = None
		self.sarah_charge_preference = None
		self._check_attributes()

	def _check_attributes(self):
		# check for allowed attribute values
		assert self.type in ('S', 'F')
		assert self.su2_multiplicity in (1, 2, 3, None)
		assert self.z2 in (-1, 1)
		assert not (self.real and self.is_adjoint)

	@property
	def original_field(self):
		return self.adjoint if self.is_adjoint else self

	@property
	def adjoint(self):
		# real scalar s: s^† = s
		# valid for real singlets and real triplets in matrix form
		if self.real:
			return self.from_field(self)
		return self.attr(
			is_adjoint=not self.is_adjoint, hypercharge=-self.hypercharge,
			u1=tuple(-q for q in self.u1), su3=-self.su3
		)

	@property
	def components(self):
		# SU(2) n-plet has n = 2j + 1 and T_3 = -j, …, j in integer steps
		orig = self.original_field
		n = self.su2_multiplicity
		j = Fraction(n - 1, 2)
		components = [SU2FieldComponent(orig, -j + i) for i in range(n)]
		if self.is_adjoint:
			components = [c.adjoint for c in components]
		components.reverse()
		# propagate name definitions for SARAH
		n_None = n * [None]
		for c, sym_c, sym_m, sym_d in zip(
			components,
			self.sarah_component_symbols if self.sarah_component_symbols else
				n_None,
			self.sarah_mixing_symbols if self.sarah_mixing_symbols else
				n_None,
			self.sarah_dirac_spinor_symbols
				if self.sarah_dirac_spinor_symbols else
				n_None
		):
			c.sarah_symbol = sym_c
			c.sarah_mixing_symbols = sym_m
			c.sarah_dirac_spinor_symbols = sym_d
			c.sarah_vev_symbols = self.sarah_vev_symbols
			c.sarah_charge_preference = self.sarah_charge_preference
		# for neutral fields, components with opposite T₃ are adjoints
		# (e.g. triplets: (Δ^+)^† = Δ^-)
		if self.neutral:
			components[int(j + 1):] = [
				c.adjoint for c in components[:int(j + 0.5)]
			]
		assert len(components) == n
		return components

	@property
	def scalar(self):
		return self.type == 'S'

	@property
	def fermion(self):
		return self.type == 'F'

	@property
	def su2_singlet(self):
		return self.su2_multiplicity == 1

	@property
	def su2_doublet(self):
		return self.su2_multiplicity == 2

	@property
	def su2_triplet(self):
		return self.su2_multiplicity == 3

	@property
	def Y(self):
		return self.hypercharge

	@property
	def quantum_numbers(self):
		return (self.type, self.su2_multiplicity, self.Y, self.z2, self.u1)

	@property
	# uncharged under U(1) groups
	def neutral(self):
		return self.Y == 0 and all(q == 0 for q in self.u1) and self.su3 == 0

	@property
	def real(self):
		return self.scalar and self.neutral and not self.su2_doublet

	def attr(self, **kw):
		cp = self.from_field(self)
		for key, val in kw.items():
			setattr(cp, key, val)
		cp._check_attributes()
		return cp

	def is_equivalent(self, other):
		return self.quantum_numbers in (
			other.quantum_numbers, other.adjoint.quantum_numbers
		)

	def to_tuple(self):
		return (self.symbol,) + self.quantum_numbers + (self.is_adjoint,)

	def __eq__(self, other):
		return isinstance(other, Field) and self.to_tuple() == other.to_tuple()

	def __hash__(self):
		return hash(self.to_tuple())

	def __repr__(self):
		return self._repr_str.format(type(self).__name__, *self.to_tuple())

	def __str__(self):
		return output_plain.Formatter.format_field(self)

def str_iterable(it):
	return ', '.join(str(f) for f in it)

# A ScalarField represents a Lorentz-scalar SU(2) multiplet.
class ScalarField(Field):
	def __init__(
		self, symbol, su2_multiplicity, Y, z2=-1, u1=(), is_adjoint=False
	):
		super().__init__(symbol, 'S', su2_multiplicity, Y, z2, u1, is_adjoint)

# A FermionField represents a Weyl fermion SU(2) multiplet.
class FermionField(Field):
	def __init__(
		self, symbol, su2_multiplicity, Y, z2=-1, u1=(), is_adjoint=False
	):
		super().__init__(symbol, 'F', su2_multiplicity, Y, z2, u1, is_adjoint)

# A DiracFermionField represents a Dirac fermion SU(2) multiplet.
DiracFermionField = collections.namedtuple('DiracFermionField',
	'left, right'
)

# A VectorLikeFermionField represents a vector-like Dirac fermion
# SU(2) multiplet, i.e. both the left-handed and the right-handed components
# of the Dirac fermion have the same quantum numbers.
class VectorLikeFermionField(DiracFermionField):
	def __new__(
		cls, symbol, su2_multiplicity, Y, z2=-1, u1=(), is_adjoint=False,
		bsm=False
	):
		# left-handed Weyl spinor
		left = FermionField(
			symbol + '₁', su2_multiplicity, Y, z2, u1, is_adjoint
		)
		# (adjoint of the) right-handed Weyl spinor
		right = FermionField(
			symbol + '₂', su2_multiplicity, -Y, z2, [-q for q in u1],
			is_adjoint
		)
		left.bsm = bsm
		right.bsm = bsm
		result = super().__new__(cls, left, right.adjoint)
		return result

	@classmethod
	def from_field(cls, field, bsm=False):
		assert field.fermion
		return cls(
			field.symbol, field.su2_multiplicity, field.Y, z2=field.z2,
			u1=field.u1, is_adjoint=field.is_adjoint, bsm=bsm
		)

ComplexScalarField = collections.namedtuple('ComplexScalarField',
	'scalar, pseudoscalar'
)

class ElectricallyChargedField(Field):
	@property
	def neutral(self):
		return self.charge == 0 and all(q == 0 for q in self.u1)

	@property
	def charge_suffix(self):
		charge = self.charge
		if charge == int(charge):
			if charge == 0:
				suffix = '⁰'
			else:
				suffix = abs(charge) * ('⁺' if charge > 0 else '⁻')
		else:
			suffix = '{:+.3g}'.format(float(charge))
		return suffix

# An SU2FieldComponent represents a component of an SU(2) multiplet.
class SU2FieldComponent(ElectricallyChargedField):
	_repr_str = (
		'{}({!r}, {!r}, {!r}, Y={!r}, z2={!r}, u1={!r}, T3={!r}, '
		'is_adjoint={!r})'
	)

	def __init__(self, field, T3):
		self.T3 = int(T3) if T3 == int(T3) else T3
		super().__init__(
			field.symbol, field.type, field.su2_multiplicity, field.Y,
			field.z2, field.u1, field.is_adjoint
		)
		self.bsm = field.bsm
		self.generations = field.generations
		# set symbol after constructor (so that charge is initialized)
		self.symbol += self.charge_suffix

	@property
	def adjoint(self):
		adjoint = super().adjoint
		adjoint.T3 = -adjoint.T3
		return adjoint

	@property
	def real(self):
		# note: neutral component of a complex field is still complex, i.e.
		# all of Q, T3 and Y must be zero (which happens if any two of them
		# are zero)
		return self.scalar and self.neutral and self.Y == 0

	@property
	def charge(self):
		result = Fraction(self.Y, 2) + self.T3
		return int(result) if result == int(result) else result

	@property
	def quantum_numbers(self):
		return super().quantum_numbers + (self.T3,)

	@property
	def components(self):
		orig = self.original_field
		if self.scalar and self.neutral:
			return [x for x in self.complex_parts if isinstance(x, Field)]
		else:
			result = EWSBField(
				orig.symbol, orig.type, orig.charge, orig.z2, orig.u1
			).attr(
				bsm=orig.bsm,
				generations=orig.generations,
				sarah_symbol=orig.sarah_symbol,
				sarah_mixing_symbols=orig.sarah_mixing_symbols,
				sarah_dirac_spinor_symbols=orig.sarah_dirac_spinor_symbols,
				sarah_charge_preference=orig.sarah_charge_preference,
			)
			if self.is_adjoint:
				result = result.adjoint
			return [result]

	@property
	def complex_parts(self):
		if self.fermion or not self.neutral:
			raise ValueError(
				'Fermion or charged field cannot be split into real and '
				'imaginary parts'
			)
		assert self.scalar
		# complex neutral scalar: split into real and imaginary (pseudoscalar)
		# parts
		scalar = pseudoscalar = EWSBField(
			self.symbol, self.type, Q=self.charge, z2=self.z2, u1=self.u1
		).attr(sarah_vev_symbols=self.sarah_vev_symbols, bsm=self.bsm)
		if self.sarah_vev_symbols:
			sym_v, sym_p, sym_s = self.sarah_vev_symbols
			scalar = scalar.attr(sarah_symbol=sym_s)
			pseudoscalar = scalar.attr(sarah_symbol=sym_p)
		if self.real:
			return ComplexScalarField(scalar=scalar, pseudoscalar=0)
		else:
			return ComplexScalarField(
				scalar=scalar.attr(symbol=self.symbol + REAL_PART_SUFFIX),
				pseudoscalar=pseudoscalar.attr(
					symbol=self.symbol + IMAG_PART_SUFFIX
				)
			)

	@property
	def gets_vev(self):
		return self.scalar and self.neutral and self.z2 == 1

	def __str__(self):
		return output_plain.Formatter.format_field(self)

# An EWSBField represents a field which is a representation of the unbroken
# symmetry groups after EWSB.
class EWSBField(ElectricallyChargedField):
	_repr_str = '{}({!r}, {!r}, Q={!r}, z2={!r}, u1={!r}, is_adjoint={!r})'

	def __init__(
		self, symbol, lorentz_type, Q, z2=-1, u1=(), is_adjoint=False
	):
		# charge should be set before calling the constructor
		self.charge = Q
		super().__init__(
			symbol, lorentz_type, None, Y=None, z2=z2, u1=u1,
			is_adjoint=is_adjoint
		)

	@property
	def adjoint(self):
		if self.real:
			return self.from_field(self)
		return self.attr(
			is_adjoint=not self.is_adjoint, charge=-self.charge,
			u1=tuple(-q for q in self.u1))

	@property
	def components(self):
		return None

	@property
	def quantum_numbers(self):
		return (self.type, self.charge, self.z2, self.u1)

# A MixedField represents a mass eigenstate after EWSB.
class MixedField(EWSBField):
	def __init__(self, gauge_es, symbol_base=None, symbol_suffix=''):
		gauge_es_orig = gauge_es
		f = gauge_es[0]
		mixing = sum(f.generations for f in gauge_es) > 1
		# set symbol
		if symbol_base is None:
			symbol_base = MIX_SCALAR_NAME if f.scalar else MIX_FERMION_NAME
		if mixing:
			symbol = symbol_base + f.charge_suffix + symbol_suffix
		else:
			symbol = f.symbol
		# call constructor, set attributes
		super().__init__(
			symbol, f.type, f.charge, z2=f.z2, u1=f.u1, is_adjoint=False
		)
		self.gauge_es = tuple(gauge_es)
		self.bsm = sum(f.bsm for f in self.gauge_es)
		if not mixing:
			self.sarah_symbol = f.sarah_symbol
		# propagate name definitions for SARAH
		for f in self.gauge_es:
			if f.sarah_mixing_symbols:
				self.sarah_mixing_symbols = f.sarah_mixing_symbols
				self.sarah_symbol = f.sarah_mixing_symbols[0]
			if f.sarah_dirac_spinor_symbols:
				self.sarah_dirac_spinor_symbols = f.sarah_dirac_spinor_symbols
			if f.sarah_charge_preference:
				self.sarah_charge_preference = f.sarah_charge_preference

