""" The macrodemos package setup.
Based on setuptools

Randall Romero-Aguilar, 2016-2020
"""

from setuptools import setup
from codecs import open


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='macrodemos',
    version='2020.04',
    description='Demos to learn macroeconomic and macroeconometric concepts',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Randall Romero-Aguilar',
    author_email='randall.romero@outlook.com',
    url='http://randall-romero.com/code/macrodemos',
    license='MIT',
    keywords='time series, ARMA',
    packages=['macrodemos'],
    python_requires='>=3.7',
    install_requires=['pandas', 'numpy', 'plotly', 'dash', 'statsmodels'],
    include_package_data=False
)



