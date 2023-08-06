import itertools
from fractions import Fraction
from .. import output
from .. import terms


class PlainFormatter(output.Formatter):
	FORMAT_OPT = {
		'linebreak': '\n',
		'param_symbol_mass': 'M',
		'param_symbol_yukawa': 'y',
		'param_symbol_coupling': 'λ',
		'join_str': ' - ',
		'join_str_hc': ' + ',
	}

	@classmethod
	def _format_product_abab(self, product):
		return '({} {})²'.format(*product[:2])

	@classmethod
	def _format_product_default(self, product):
		parts = []
		for x, g in itertools.groupby(product):
			g = list(g)
			if x.scalar:
				p_str = self.format_field(x)
				if len(g) > 1:
					p_str += self.format_superscript(len(g))
			else:
				p_str = ' '.join(self.format_field(x) for x in g)
			parts.append(p_str)
		return ' '.join(parts)

	@classmethod
	def _format_product_triplet(self, product, intermediate):
		return 'Tr({})'.format(intermediate)

	@classmethod
	def _format_term_default(self, term):
		term_strs = []
		for pr in term:
			pr_str = self.format_product(pr)
			# print SU(2) scalar products in interaction terms in parentheses
			if len(term) > 1 and len(pr) >= 2 and not (
				all(x.scalar and (x.su2_singlet or x.su2_triplet) for x in pr)
			):
				term_strs.append('({})'.format(pr_str))
			else:
				term_strs += [pr_str]
		return ' '.join(term_strs)

	@classmethod
	def _format_term_squared(self, term):
		product = term[0]
		if all(x.su2_triplet for x in product):
			return '{}²'.format(product)
		else:
			return '({})²'.format(product)

	@classmethod
	def _format_term_hc(self, term, param_str):
		return '({}{} + H.c.)'.format(param_str, self.format_term(term))

	@classmethod
	def format_field(self, field):
		symbol = field.symbol
		if field.is_adjoint:
			return '{}^†'.format(symbol)
		else:
			return symbol

	@classmethod
	def format_prefix(self, prefix):
		if prefix == Fraction(1, 2):
			return '½ '
		else:
			return super().format_prefix(prefix)

	@classmethod
	def format_subscript(self, subscript):
		if isinstance(subscript, int):
			return output.int_to_scripts(subscript, output.SUBSCRIPTS)
		else:
			return super().format_subscript(subscript)

	@classmethod
	def format_superscript(self, superscript):
		if isinstance(superscript, int):
			return output.int_to_scripts(superscript, output.SUPERSCRIPTS)
		else:
			return super().format_superscript(superscript)

	@classmethod
	def format_symbol(self, symbol):
		return symbol

Formatter = PlainFormatter
terms.FORMATTER = PlainFormatter

