from setuptools import setup, find_packages
import os

version = "1.0.0.2"


setup(
    name='dtg',
    version=version,
    description='Heavy-tailed distribution analysis',
    author='Maxim Ryzhov',
    author_email='ryzhov@phystech.edu',
    license='MIT',
    packages=find_packages(),
    url='https://gitlab.com/BoBeni/DTG',
    install_requires=['numpy', 'rd-pr', 'scipy'],
    zip_safe=False
)
