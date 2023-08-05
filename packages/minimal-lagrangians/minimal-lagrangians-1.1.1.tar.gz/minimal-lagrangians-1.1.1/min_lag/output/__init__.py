import abc
import collections
from fractions import Fraction
from .. import terms
from ..terms import TermTypes
from ..unicode_util import *


class Parameter:
	def __init__(self, prefix, name, subscript, superscript, term_type):
		self.prefix = prefix
		self.name = name
		self.subscript = subscript
		self.superscript = superscript
		self.term_type = term_type

	def __str__(self):
		return ' '.join(str(x)
			for x in (self.prefix, self.name, self.subscript, self.superscript)
		)


class Formatter(abc.ABC):
	@classmethod
	@abc.abstractmethod
	def _format_opt(self, key):
		return self.FORMAT_OPT[key]

	@classmethod
	@abc.abstractmethod
	def _format_product_default(self, product):
		raise NotImplementedError

	@classmethod
	def _format_product_abab(self, product):
		return self._format_product_default(product)

	@classmethod
	def _format_product_triplet(self, product, intermediate):
		return intermediate

	@classmethod
	@abc.abstractmethod
	def _format_term_default(self, term):
		raise NotImplementedError

	@classmethod
	def _format_term_squared(self, term):
		return self._format_term_default(term)

	@classmethod
	def _format_term_hc(self, term, param_str):
		return '({}{}{}{})'.format(
			param_str, self.format_term(term), self._format_opt('join_str_hc'),
			self.format_term(term.adjoint)
		)

	# returns a tuple of the form
	# (formatted Lagrangian as a string, list of parameter names)
	@classmethod
	def _format_lagrangian(
		self, model, lagrangian, param_idx=0, param_idx_list=None, **kwargs
	):
		# TODO fix or remove param_idx parameter
		assert param_idx == 0 or param_idx_list is None
		opt = self._format_opt
		result = []
		parameters = []
		prev_term_type = None
		param_idx_glob = -1
		param_idx_yukawa = 0
		param_idx_coupling = 0
		for term in lagrangian:
			param_idx_glob += 1
			# skip (+ H.c.) terms – these are already handled by format_term
			# with Hc=True
			if term.adjoint in lagrangian.add_hc: continue
			curr_term_type = term.term_type
			if prev_term_type and curr_term_type is not prev_term_type:
				result[-1] += opt('linebreak')
			prev_term_type = curr_term_type
			param_pre = ''
			param_superscript = ''
			# mass terms
			if curr_term_type.mass_term:
				param_symbol = opt('param_symbol_mass')
				# mass term with identical fields
				if all(x.symbol == pr[0].symbol for pr in term for x in pr):
					f = term[0][0]
					param_subscript = f.adjoint if f.is_adjoint else f
					# real scalar or Majorana mass terms
					if all(x == pr[0] for pr in term for x in pr):
						param_pre = Fraction(1, 2)
					if f.scalar:
						param_superscript = 2
				# mass term with different fields (→ mixing)
				else:
					param_subscript = term
			else:
				if curr_term_type == TermTypes.YUKAWA:
					param_idx_yukawa += 1
					param_idx = param_idx_yukawa
					param_symbol = opt('param_symbol_yukawa')
				else:
					param_idx_coupling += 1
					param_idx = param_idx_coupling
					param_symbol = opt('param_symbol_coupling')
				param_subscript = (
					param_idx if param_idx_list is None else
					param_idx_list[param_idx_glob]
				)
			param = Parameter(
				param_pre, param_symbol, param_subscript, param_superscript,
				curr_term_type
			)
			parameters.append(param)
			result.append(
				self.format_term(term, param, Hc=term in lagrangian.add_hc)
			)
		return opt('join_str').join([''] + result), parameters

	@classmethod
	def _format_script(self, script):
		if hasattr(script, 'fields'):   # script is a term
			return ''.join(self.format_symbol(f.symbol) for f in script.fields)
		elif hasattr(script, 'symbol'): # script is a field
			return self.format_field(script)
		else:
			return self.format_symbol(str(script))

	@classmethod
	@abc.abstractmethod
	def format_field(self, field):
		raise NotImplementedError

	@classmethod
	def format_parameter(self, param, prefix=True):
		if prefix:
			format_prefix = self.format_prefix(param.prefix)
		else:
			format_prefix = ''
		param_str = '{}{}{}{}'.format(
			format_prefix, self.format_parameter_symbol(param.name),
			self.format_subscript(param.subscript),
			self.format_superscript(param.superscript)
		)
		return param_str

	@classmethod
	def format_prefix(self, prefix):
		if prefix:
			return self.format_symbol(str(prefix)) + ' '
		else:
			return ''

	@classmethod
	def format_product(self, product):
		# print a product like Δ^† Δ Δ^† Δ as (Δ^† Δ)²
		if len(product) == 4 and product[:2] == product[2:] and (
			not all(x == product[0] for x in product)
		):
			result = self._format_product_abab(product)
		# print products of scalars where all fields are the same usin
		# exponents
		else:
			result = self._format_product_default(product)
		# print trace around pure triplet products
		if all(x.su2_triplet for x in product):
			result = self._format_product_triplet(product, result)
		return result

	@classmethod
	def format_parameter_symbol(self, symbol):
		return self.format_symbol(symbol)

	@classmethod
	def format_subscript(self, subscript):
		if subscript:
			return '_{}'.format(self._format_script(subscript))
		else:
			return ''

	@classmethod
	def format_superscript(self, superscript):
		if superscript:
			return '^{}'.format(self._format_script(superscript))
		else:
			return ''

	@classmethod
	@abc.abstractmethod
	def format_symbol(self, symbol):
		raise NotImplementedError

	@classmethod
	def format_term(self, term, param=None, Hc=False):
		if param is None:
			param_str = ''
		else:
			param_str = self.format_parameter(param) + ' '
		# allow (+ H.c.) terms to be formatted specially
		if Hc:
			return self._format_term_hc(term, param_str)
		# print a squared term if it consists of two identical products,
		# e.g. (H^† H) (H^† H) = (H^† H)²
		if (
			len(term) == 2 and len(term[0]) == len(term[1]) == 2 and
			term[0] == term[1]
		):
			result = self._format_term_squared(term)
		else:
			result = self._format_term_default(term)
		return param_str + result

	@classmethod
	def format_lagrangian(self, model, lagrangian, **kwargs):
		result, _ = self._format_lagrangian(model, lagrangian, **kwargs)
		return result

