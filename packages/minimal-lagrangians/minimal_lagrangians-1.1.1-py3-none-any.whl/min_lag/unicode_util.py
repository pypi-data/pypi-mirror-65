GREEK = list('ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωϑϕϰϱ')
SUPERSCRIPTS = list('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻')
SUBSCRIPTS   = list('₀₁₂₃₄₅₆₇₈₉')
SCRIPT_TO_DIGIT = {'⁺': '+', '⁻': '-'}
for i in range(10):
	SCRIPT_TO_DIGIT[SUPERSCRIPTS[i]] = str(i)
	SCRIPT_TO_DIGIT[SUBSCRIPTS[i]] = str(i)

def int_to_scripts(num, script_digits):
	return ''.join(script_digits[int(str_digit)] for str_digit in str(num))

def scripts_to_int(script_str):
	return int(''.join(
		SCRIPT_TO_DIGIT[script_str[i]] for i in range(len(script_str))
	))

