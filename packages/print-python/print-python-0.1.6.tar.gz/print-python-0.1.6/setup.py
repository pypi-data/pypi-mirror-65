import setuptools

with open('README.md', 'r') as fh:
	readme = fh.read()

setuptools.setup(
	name='print-python',
	version='0.1.6',
	author='Georges Duverger',
	author_email='georges.duverger@gmail.com',
	description='Print Python client',
	long_description=readme,
	long_description_content_type='text/markdown',
	url='https://github.com/gduverger/print-python',
	license='MIT',
	packages=['print'],
	# install_requires=[],
	python_requires='>=3',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Intended Audience :: Developers',
		'Natural Language :: English'
	],
)
