from distutils.core import setup

from setuptools import find_packages


install_requires = [
    "django>=1.11, <2.0",
]

extras_require = {
    'test': ['mock >=1']
}


setup(
    name='django-settings-composer',
    version='2.0.0',
    author='Colin Barnwell',
    description="A 'sensible' way to gather settings dynamically",
    long_description=open('README.md').read(),
    packages=find_packages(),
    scripts=[],
    python_requires='>=3.7.0',
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=extras_require['test']
)
