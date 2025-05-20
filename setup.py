from setuptools import find_packages
from setuptools import setup

setup(
    name='django-settings-composer',
    version='2.1.0',
    author='Colin Barnwell',
    description="A 'sensible' way to gather settings dynamically",
    long_description=open('README.md').read(),
    packages=find_packages(),
    scripts=[],
    install_requires = [
        "django<3",
    ],
    extras_require={
        "testing": [
            "mock",
            "pytest",
            "pytest-django",
        ]
    },
)
