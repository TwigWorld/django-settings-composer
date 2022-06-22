from distutils.core import setup

from setuptools import find_packages


install_requires = [
    "django >=1.6, <2.3",
]

extras_require = {
    'test': ['mock >=1']
}


setup(
    name='django-settings-composer',
    version='1.0.3',
    author='Colin Barnwell',
    description="A 'sensible' way to gather settings dynamically",
    long_description=open('README.md').read(),
    packages=find_packages(),
    scripts=[],
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=extras_require['test']
)
