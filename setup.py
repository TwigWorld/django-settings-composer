from distutils.core import setup

from setuptools import find_packages


install_requires = [
    "Django >=1.6 <=1.9",
]

extras_require = {
    'test': ['mock >=1']
}


setup(
    name='django-settings-composer',
    version='0.9.0',
    author='Colin Barnwell',
    description="A 'sensible' way to gather settings dynamically",
    long_description=open('README.md').read(),
    packages=find_packages(),
    scripts=[],
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=extras_require['test']
)
