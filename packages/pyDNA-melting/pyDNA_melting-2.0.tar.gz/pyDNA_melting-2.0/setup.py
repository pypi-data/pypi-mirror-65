from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyDNA_melting',
    version='2.0',
    author='Yichao Li',
    author_email='yl079811@ohio.edu',
    url='https://github.com/YichaoOU/pyDNA_melting',
	packages=['pyDNA_melting'],
    license='LICENSE',
	scripts=['DNA_melting'],
	package_data={'': ["scripts/*"]},
	include_package_data=True,
    description='Calculate DNA melting score',
	long_description=long_description,
	long_description_content_type='text/markdown'	,
)


# python setup.py sdist
# python setup.py bdist_wheel --universal
# test the distributions
# twine upload dist/*

