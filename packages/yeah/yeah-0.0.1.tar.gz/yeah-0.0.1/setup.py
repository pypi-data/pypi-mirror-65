import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='yeah',
    version='0.0.1',
    author='Muchen Sun',
    description='yeah!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'jax',
    ],
    url='https://github.com/MuchenSun/yeah',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
