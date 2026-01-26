from setuptools import setup, find_packages

setup(
    name='alt-package-compare',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.28.0',
        'setuptools>=80.10.2'
    ],
    entry_points={
        'console_scripts': [
            'branch-compare=src.main:main',
        ],
    },
)