#!/usr/bin/env python3
import argparse
import importlib
import os.path
import pkgutil
import sys
import textwrap
import warnings
from pathlib import Path
import min_lag.data as data
import min_lag.fields as fields
import min_lag.models as models
import min_lag.output as output
from min_lag import __version__

LIST_MODELS_VALUE = 'list'
DEFAULT_MODEL_FILE_NAME = 'models.py'
EVAL_GLOBALS = {
	'FermionField': fields.FermionField,
	'ScalarField': fields.ScalarField,
	'BSMModel': models.BSMModel,
}

output_modules = [info[1] for info in pkgutil.iter_modules(output.__path__)]
# parse command line arguments
parser = argparse.ArgumentParser(description='A Python program to generate '
	'the Lagrangians for dark matter models')
model_arg = parser.add_argument('model', metavar='model',
	help='name of the model whose Lagrangian is to be generated (specify '
		'“{}” in order to list all available models)'.format(LIST_MODELS_VALUE)
		)
parser.add_argument('alpha', metavar='parameter α', type=int, nargs='?',
	help='value of the model parameter α (determines hypercharges of the '
		'fields)')
parser.add_argument('--format', choices=output_modules, default='plain',
	help='output format for the generated Lagrangian (default: plain)')
parser.add_argument('--model-file', metavar='path/to/file.py', nargs='?',
	type=Path, const=Path(DEFAULT_MODEL_FILE_NAME),
	help='file containing user-defined models; a file is only read if this '
		'option is present (default: {})'.format(
			os.path.join('.', DEFAULT_MODEL_FILE_NAME)
		))
parser.add_argument('--omit-equivalent-scalars', action='store_true',
	help='keep only scalar fields from the model which have unique quantum '
		'numbers and absolute hypercharge values (omit duplicates)')
parser.add_argument('--omit-self-interaction', action='store_true',
	help='omit pure self-interactions of the new fields in the Lagrangian, '
		'that is, output only interaction terms which involve both SM and new '
		'fields (default: output all terms)')
parser.add_argument('--list-discarded-terms', action='store_true',
	help='list redundant terms which were discarded from the Lagrangian due '
		'to identities')
parser.add_argument('--sarah-no-scalar-cpv', action='store_true',
	help='assume that there is no CP violation causing mixing between scalar '
		'and pseudoscalar fields for SARAH output')
parser.add_argument('--version', action='version',
	version='%(prog)s v{}'.format(__version__),
	help='show program’s version number and exit')
args = parser.parse_args()

# parse model file if desired
if args.model_file is not None:
	model_file_str = args.model_file.read_text()
	model_file_list = eval(model_file_str, EVAL_GLOBALS)
	data.append(model_file_list)

# check args.model using potentially updated data
model_names = sorted(data.DATA.keys())
model_arg.choices = model_names + [LIST_MODELS_VALUE]
parser.parse_args()
if args.model == LIST_MODELS_VALUE:
	print('Available models are:')
	for model_name in model_names:
		print('\t' + model_name)
	sys.exit(0)

# if a model with parameters has been selected, the parameter α must be
# specified
if data.DATA[args.model].param_values and args.alpha is None:
	parser.print_usage(file=sys.stderr)
	print(
		'Error: The parameter α must be specified for model {}'.format(
			args.model
		), file=sys.stderr
	)
	sys.exit(2)

# create a dict of the models in data.py
all_models = [model.implement(alpha) for model in data.DATA.values()
	for alpha in model.param_values]
all_models += [model for model in data.DATA.values() if not model.param_values]
all_models = {
	(model.original_name, model.imp_param_value): model for model in all_models
}

# select model
param_values = data.DATA[args.model].param_values
# print error message for wrong value of α
if param_values and not args.alpha in param_values:
	print(
		'Error: Invalid value for parameter α: {} (choose from {})'.format(
			args.alpha, param_values
		), file=sys.stderr
	)
	sys.exit(3)
model = all_models[args.model, args.alpha]
if args.omit_equivalent_scalars:
	model.omit_equivalent_scalars()

# check for Witten SU(2) anomaly
if model.anomalies:
	if models.Anomalies.GAUGE_ANOMALY_HYPERCHARGE in model.anomalies:
		warnings.warn(
			'Made some fermions vector-like in order to cancel gauge '
			'anomalies.\n'
			'The following fields were made vector-like: ' +
			fields.str_iterable(
				model.anomalies[models.Anomalies.GAUGE_ANOMALY_HYPERCHARGE]
			)
		)
	if models.Anomalies.WITTEN_ANOMALY in model.anomalies:
		warnings.warn(
			'Made a fermion doublet vector-like in order to cancel the Witten '
			'SU(2) anomaly.\n'
			'The following field was made vector-like: ' +
			str(next(iter(model.anomalies[models.Anomalies.WITTEN_ANOMALY])))
		)

# format and print selected Lagrangian
output_imp = importlib.import_module('min_lag.output.{}'.format(args.format))
L = model.lagrangian()
if args.omit_self_interaction:
	L = L.without_self_interaction()
print(
	output_imp.Formatter.format_lagrangian(
		model, L, sarah_no_scalar_cpv=args.sarah_no_scalar_cpv
	)
)
# print discarded terms if desired
if args.list_discarded_terms:
	print()
	if L.discarded_terms:
		if len(L.discarded_terms) > 1:
			plural1 = 'terms (' + str(len(L.discarded_terms)) + ') were'
			plural2 = 'them'
		else:
			plural1 = 'term was'
			plural2 = 'it'
		print(textwrap.fill(
			'The following ' + plural1 + ' discarded from the Lagrangian due '
			'to identities making ' + plural2 + ' redundant:'
		))
		print(L.discarded_terms)
	else:
		print(textwrap.fill(
			'No terms were discarded from the Lagrangian for being redundant '
			'due to identities.'
		))

