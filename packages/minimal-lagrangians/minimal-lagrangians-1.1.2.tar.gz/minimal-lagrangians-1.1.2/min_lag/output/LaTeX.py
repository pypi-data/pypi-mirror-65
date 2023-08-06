import itertools
from .. import output
from fractions import Fraction


GREEK_LATEX = [
	'A', 'B', r'\Gamma', r'\Delta', 'E', 'Z', 'H', r'\Theta', 'I', 'K',
	r'\Lambda', 'M', 'N', r'\Xi', 'O', r'\Pi', 'P', r'\Sigma', 'T', r'\Upsilon',
	r'\Phi', 'X', r'\Psi', r'\Omega',
	r'\alpha', r'\beta', r'\gamma', r'\delta', r'\varepsilon', r'\zeta', r'\eta',
	r'\theta', r'\iota', r'\kappa', r'\lambda', r'\mu', r'\nu', r'\xi', 'o',
	r'\pi', r'\rho', r'\sigma', r'\tau', r'\upsilon', r'\varphi', r'\chi',
	r'\psi', r'\omega',
	r'\vartheta', r'\phi', r'\varkappa', r'\varrho',
]
SYMBOLS = ['−']
SYMBOLS_LATEX = ['-']
assert len(output.GREEK) == len(GREEK_LATEX), \
	'{} ≠ {}'.format(len(output.GREEK), len(GREEK_LATEX))
assert len(SYMBOLS) == len(SYMBOLS_LATEX), \
	'{} ≠ {}'.format(len(SYMBOLS), len(SYMBOLS_LATEX))
GREEK_TO_LATEX = {
	output.GREEK[i]: GREEK_LATEX[i] for i in range(len(output.GREEK))
}
SYMBOLS_TO_LATEX = {SYMBOLS[i]: SYMBOLS_LATEX[i] for i in range(len(SYMBOLS))}
TO_REPLACE = output.GREEK + SYMBOLS
CONVERT_TO_LATEX = {}
CONVERT_TO_LATEX.update(GREEK_TO_LATEX)
CONVERT_TO_LATEX.update(SYMBOLS_TO_LATEX)

class LaTeXFormatter(output.Formatter):
	FORMAT_OPT = {
		'linebreak': '\n',
		'param_symbol_mass': r'M',
		'param_symbol_yukawa': r'y',
		'param_symbol_coupling': r'\lambda',
		'join_str': ' - ',
		'join_str_hc': ' + ',
	}

	@classmethod
	def _format_product_abab(self, product):
		field_str = [self.format_field(f) for f in product]
		return r'\left({} {}\right)^2'.format(*field_str[:2])

	@classmethod
	def _format_product_default(self, product):
		parts = []
		for x, g in itertools.groupby(product):
			g = list(g)
			if x.scalar:
				p_str = self.format_field(x)
				if len(g) > 1:
					p_str = '{%s}^%d' % (p_str, len(g))
			else:
				p_str = ' '.join(self.format_field(x) for x in g)
			parts.append(p_str)
		return ' '.join(parts)

	@classmethod
	def _format_product_triplet(self, product, intermediate):
		return r'\operatorname{Tr}\left(%s\right)' % intermediate

	@classmethod
	def _format_term_default(self, term):
		term_strs = []
		for pr in term:
			pr_str = self.format_product(pr)
			# print SU(2) scalar products in interaction terms in parentheses
			if len(term) > 1 and len(pr) >= 2 and not (
				all(x.scalar and (x.su2_singlet or x.su2_triplet) for x in pr)
			):
				term_strs.append(r'\left({}\right)'.format(pr_str))
			else:
				term_strs += [pr_str]
		return ' '.join(term_strs)

	@classmethod
	def _format_term_squared(self, term):
		product = term[0]
		product_str = self.format_product(product)
		if all(x.su2_triplet for x in product):
			return '{}^2'.format(product_str)
		else:
			return r'\left({}\right)^2'.format(product_str)

	@classmethod
	def _format_term_hc(self, term, param_str):
		return r'\left(%s%s + \text{H.\,c.}\right)' % (
			param_str, self.format_term(term)
		)

	@classmethod
	def format_field(self, field):
		symbol = self.format_symbol(field.symbol)
		if field.is_adjoint:
			return r'{%s}^\dagger' % symbol
		else:
			return symbol

	@classmethod
	def format_prefix(self, prefix):
		if isinstance(prefix, Fraction):
			return r'\frac{%d}{%d} ' % (prefix.numerator, prefix.denominator)
		else:
			return super().format_prefix(prefix)

	@classmethod
	def format_subscript(self, subscript):
		if subscript:
			return '_{%s}' % self._format_script(subscript)
		else:
			return ''

	@classmethod
	def format_superscript(self, superscript):
		if superscript:
			return '^{%s}' % self._format_script(superscript)
		else:
			return ''

	@classmethod
	def format_symbol(self, symbol):
		result = ''
		opening_braces = 0
		for letter in symbol:
			if letter in TO_REPLACE:
				result += CONVERT_TO_LATEX[letter]
			elif letter in output.SUPERSCRIPTS:
				result += '^' + output.SCRIPT_TO_DIGIT[letter] + '}'
				opening_braces += 1
			elif letter in output.SUBSCRIPTS:
				result += '_' + output.SCRIPT_TO_DIGIT[letter] + '}'
				opening_braces += 1
			else:
				result += letter
		return ('{' * opening_braces) + result

Formatter = LaTeXFormatter

