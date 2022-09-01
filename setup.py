# Minimal setup.py to fix import issues

from setuptools import setup, find_packages


setup(
    name='mylava',
    version='1.0.0',
    url='https://github.com/jacobpennington/lava-scripts.git',
    author='Jacob Pennington',
    author_email='jacob.p.neuro@gmail.com',
    description='Misc lava scripts and subclasses.',
    packages=find_packages(),    
    install_requires=[],
)
