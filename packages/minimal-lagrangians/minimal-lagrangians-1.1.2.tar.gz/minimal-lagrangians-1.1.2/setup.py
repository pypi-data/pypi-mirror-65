#!/usr/bin/env python3
import setuptools

with open('README.md') as f:
	long_description = f.read()

setuptools.setup(
	name='minimal-lagrangians',
	author='Simon May',
	author_email='simon.may@mpa-garching.mpg.de',
	description='A Python program to generate the Lagrangians for dark matter models',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://gitlab.com/Socob/minimal-lagrangians',
	keywords='particle physics, beyond the standard model, dark matter',
	packages=setuptools.find_packages(),
	package_data={'': ['data/*']},
	license='GNU GPLv3',
	platforms='OS Independent',
	classifiers=[
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3 :: Only',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: OS Independent',
		'Topic :: Scientific/Engineering :: Physics',
		'Intended Audience :: Science/Research',
		'Natural Language :: English',
	],
	python_requires='>=3.4',
	scripts=['minimal-lagrangians', 'minimal-lagrangians.py'],
	setup_requires=['setuptools_scm'],
	use_scm_version={
		'write_to': 'min_lag/version.py',
		'write_to_template': "__version__ = '{version}'",
	},
)
