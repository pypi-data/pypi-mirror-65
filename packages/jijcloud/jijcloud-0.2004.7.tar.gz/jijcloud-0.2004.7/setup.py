from setuptools import setup, find_packages

setup(
    name="jijcloud",
    version="0.2004.7",
    install_requires=["dimod", "requests", "toml"],
    author_email='info@j-ij.com',
    author='Jij Inc.',
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests',
    license='MIT',
)
