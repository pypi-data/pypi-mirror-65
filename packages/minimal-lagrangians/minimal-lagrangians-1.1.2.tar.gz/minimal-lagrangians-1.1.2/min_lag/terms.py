import collections
import enum
import functools
import itertools
import operator


MASS_DIMENSION_MAX = 4
TermType = collections.namedtuple('TermType', 'num_scalars, num_fermions')
# bosons:   mass dimension = 1
# fermions: mass dimension = 3/2
# renormalizable if mass dimension of a term is ≤ 4
class TermTypes(enum.Enum):
	SCALAR_MASS  = TermType(2, 0)
	S3           = TermType(3, 0)
	S4           = TermType(4, 0)
	FERMION_MASS = TermType(0, 2)
	YUKAWA       = TermType(1, 2)

	@classmethod
	def from_term_comb(cls, term_comb, no_exception=False):
		num_scalars = sum(x.scalar for x in term_comb)
		num_fermions = sum(x.fermion for x in term_comb)
		term_type = TermType(num_scalars, num_fermions)
		for t in cls:
			if term_type == t.value:
				return t
		if no_exception:
			return False
		else:
			raise ValueError('Illegal term: {!r}'.format(term_comb))

	@property
	def mass_term(self):
		return self in (type(self).SCALAR_MASS, type(self).FERMION_MASS)


class DummyFormatter:
	@classmethod
	def format_product(self, product):
		return repr(product)
	@classmethod
	def format_term(self, term, param=None, Hc=False):
		return repr(term)
	@classmethod
	def _format_lagrangian(
		self, model, lagrangian, param_idx=0, param_idx_list=None
	):
		return repr(lagrangian), None

FORMATTER = DummyFormatter


# returns True if l1 and l2 are cyclic rotations of each other, False otherwise
def is_cyclic_rotation(l1, l2):
	# if the lists have different length or contain different elements,
	# return False
	if len(l1) != len(l2) or set(l1).difference(l2):
		return False
	l1, l2 = collections.deque(l1), collections.deque(l2)
	for i in range(len(l1)):
		l2.rotate()
		if l1 == l2:
			return True
	return False


# An InvariantProduct is essentially a tuple of fields representing a product
# of fields which is gauge-invariant.
# TODO: move check for invariance to this class?
class InvariantProduct(tuple):
	@staticmethod
	def sort_key(field):
		return (not field.is_adjoint, field.symbol)

	def __new__(cls, *fields):
		fields = tuple(fields)
		# make sure that singlets are always split out into a separate product
		num_singlets = sum(f.su2_singlet for f in fields)
		assert num_singlets == 0 or len(fields) == num_singlets
		if len(fields) == 2:
			# sort fields by symbol, in the order φ^† φ if possible
			fields = sorted(fields, key=cls.sort_key)
		# cosmetic: for traces of triplets, use cyclicity to get the shortest
		# representation; in a tie, try to put an adjoint field first, and
		# finally use the field names
		if all(f.su2_triplet for f in fields):
			tr = collections.deque(fields)
			rotations = []
			scores = []
			for i in range(len(tr)):
				length = sum(1 for _ in itertools.groupby(tr))
				rotations.append(tuple(tr))
				scores.append((
					length, not tr[0].is_adjoint, ''.join(f.symbol for f in tr)
				))
				tr.rotate()
			fields = rotations[scores.index(min(scores))]
		# construct object
		result = super().__new__(cls, fields)
		# use collections.Counter to represent a list where the order of
		# elements does not matter (“multiset”)
		# fields and its items need to be hashable (immutable) for this
		result._counter = collections.Counter(fields)
		result._hash = hash(frozenset(result._counter.items()))
		# assert that fields is not empty
		assert fields
		return result

	@property
	def adjoint(self):
		# taking the adjoint reverses the order of fields
		fields = [f.adjoint for f in reversed(self)]
		return type(self)(*fields)

	def get_fields(self, original=False, sort=False, unique=False):
		res = tuple(self)
		if original:
			res = tuple(field.original_field for field in res)
		if unique:
			res = tuple(set(res))
		if sort:
			res = tuple(sorted(res, key=InvariantProduct.sort_key))
		return res

	def __eq__(self, other):
		if not isinstance(other, type(self)):
			return False
		self_triplets = [f for f in self if f.su2_triplet]
		other_triplets = [f for f in other if f.su2_triplet]
		num_singlets = sum(f.su2_singlet for f in self)
		# products of triplets are invariant under cyclic permutations
		if len(self) == len(self_triplets) == len(other_triplets):
			return is_cyclic_rotation(self_triplets, other_triplets)
		# For products with ≤ 3 factors which are not all triplets, the order
		# of fields does not matter; the only options are actually:
		#   - 2 factors (+ any number of singlets, but these will always be in
		#                a separate product anyway)
		#   - DTD (order does not matter via identity 3)
		elif len(self) <= 3:
			return self._counter == other._counter
		else:
			return super().__eq__(other)

	def __hash__(self):
		return self._hash

	def __repr__(self):
		return type(self).__name__ + super().__repr__()

	def __str__(self):
		return FORMATTER.format_product(self)


# An InvariantTerm is a list of InvariantProducts and represents a term in the
# Lagrangian. As it is a product of gauge-invariant products, it too is
# gauge-invariant. In addition, an InvariantTerm is also Lorentz-invariant,
# i.e. it contains an even number of both left- and right-handed fermion
# fields. The order of InvariantProducts within the term does not matter.
class InvariantTerm(tuple):
	# key function for consistent order of products within a term
	# sorts products by (with descending importance):
	# - number of adjoint fields (descending)
	# - length (descending)
	# - number of SM fermions (ascending)
	# - total SU(2) multiplicity (descending)
	# - number of groups of factors (ascending), i.e. x² < xy
	# - string representation
	@staticmethod
	def sort_key(prod):
		return (
			-sum(f.is_adjoint for f in prod),
			-len(prod),
			sum(f.fermion for f in prod if not f.bsm),
			-sum(f.su2_multiplicity for f in prod),
			sum(1 for _ in itertools.groupby(prod)),
			# make sure that adjoint fields sort before non-adjoint ones
			str(prod).replace(' ', '').replace('^†', ' ^†'),
		)

	def __new__(cls, *products):
		products = [
			p if isinstance(p, InvariantProduct) else InvariantProduct(*p)
			for p in products if p
		]
		# sort products
		products.sort(key=cls.sort_key)
		# merge all products of scalar singlets with Y = 0 into one
		p_no_singlets = []
		p_singlets = []
		for prod in products:
			if all(
				f.scalar and f.su2_singlet and f.hypercharge == 0
				for f in prod
			):
				p_singlets += prod
			else:
				p_no_singlets.append(prod)
		if p_singlets:
			singlets_product = InvariantProduct(*p_singlets)
			products = tuple(p_no_singlets + [singlets_product])
		else:
			products = tuple(products)
		result = super().__new__(cls, products)
		result._fields = None
		# use collections.Counter to represent a list where the order of
		# elements does not matter (“multiset”)
		# products and its items need to be hashable (immutable) for this
		result._counter = collections.Counter(products)
		result._hash = hash(frozenset(result._counter.items()))
		# assert that products is not empty
		assert products
		return result

	@property
	def adjoint(self):
		# taking the adjoint reverses the order of fields
		products = [p.adjoint for p in reversed(self)]
		return type(self)(*products)

	@property
	def fields(self):
		if not self._fields:
			self._fields = tuple(field for prod in self for field in prod)
		return self._fields

	def get_fields(self, original=False, sort=False, unique=False):
		res = self.fields
		if original:
			res = tuple(field.original_field for field in res)
		if unique:
			res = tuple(set(res))
		if sort:
			res = tuple(sorted(res, key=InvariantProduct.sort_key))
		return res

	@property
	def term_type(self):
		return TermTypes.from_term_comb(self.fields)

	def to_tuples(self):
		return tuple(tuple(prod) for prod in self)

	def __eq__(self, other):
		if not isinstance(other, type(self)):
			return False
		return self._counter == other._counter

	def __hash__(self):
		return self._hash

	def __repr__(self):
		return type(self).__name__ + super().__repr__()

	def __str__(self):
		return FORMATTER.format_term(self)


# A Lagrangian is essentially a set of InvariantTerm objects.
class Lagrangian(frozenset):
	# key function to group terms by type when sorting and achieve a consistent
	# order
	@staticmethod
	def sort_key(term):
		t_type = term.term_type
		offset = 0
		# put fermion terms at the end
		if t_type in (TermTypes.FERMION_MASS, TermTypes.YUKAWA):
			offset += 10
		type_key = offset + sum(t_type.value)
		# also sort within groups so that the order stays consistent between
		# runs
		term_key = tuple(
			functools.reduce(operator.add, x)
			for x in zip(*(
				term.sort_key(p) for p in term
			))
		)
		return (type_key, term_key)

	def __new__(cls, terms, discarded_terms=()):
		terms_in = [
			t if isinstance(t, InvariantTerm) else InvariantTerm(t)
			for t in terms
		]
		terms = set(terms_in)
		# replace pairwise adjoint terms with one term which is also in add_hc
		add_hc = set()
		checked = set()
		# iterate over a copy of terms so that terms can be mutated during
		# iteration
		for term in set(terms):
			adjoint = term.adjoint
			if adjoint in checked and (
				# don’t abbreviate using + H.c. if taking the adjoint only
				# changes the order of terms
				term.get_fields(sort=True) != adjoint.get_fields(sort=True)
			):
				terms.remove(term)
				terms.remove(adjoint)
				# keep the term with fewer adjoint fields
				term_adjnum = sum(f.is_adjoint for f in term.fields)
				adjoint_adjnum = sum(f.is_adjoint for f in adjoint.fields)
				keep = adjoint if adjoint_adjnum < term_adjnum else term
				terms.add(keep)
				# record terms whose adjoint should be included in add_hc
				add_hc.add(keep)
			checked.add(term)
		result = super().__new__(cls, terms)
		result.add_hc = frozenset(add_hc)
		# remember order of insertion to obtain reproducible iteration order
		# between several executions of the program
		lst = []
		seen = set()
		for term in terms_in:
			if term not in seen and term in terms:
				lst.append(term)
			seen.add(term)
		assert len(lst) == len(terms)
		result._list = lst
		# group terms in the Lagrangian
		result._list.sort(key=result.sort_key)
		result.discarded_terms = (
			DiscardedTerms(discarded_terms) if discarded_terms
			else frozenset(discarded_terms)
		)
		return result

	def without_self_interaction(self):
		return type(self)(
			term for term in self
			if len(term.fields) == 2 or
				not all(field.bsm for field in term.fields)
		)

	def __contains__(self, item):
		return item.adjoint in self.add_hc or super().__contains__(item)

	def __iter__(self):
		# always group terms in the Lagrangian
		for term in self._list:
			yield term
			if term in self.add_hc:
				yield term.adjoint

	def __len__(self):
		# count terms with add_hc twice
		return super().__len__() + len(self.add_hc)

	def __str__(self):
		result, _ = FORMATTER._format_lagrangian(None, self)
		return result

class DiscardedTerms(Lagrangian):
	def __new__(cls, terms):
		result = super().__new__(cls, terms, discarded_terms=())
		del result.discarded_terms
		return result

	def __len__(self):
		return super(Lagrangian, self).__len__()

	def __str__(self):
		return ', '.join(
			str(term) + ' + H.c.' if term in self.add_hc else str(term)
			for term in self._list
		)

