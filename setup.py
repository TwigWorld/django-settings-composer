from distutils.core import setup

setup(
    name='django-settings-composer',
    version='0.1.0',
    author='Colin Barnwell',
    scripts=[],
    description="A 'sensible' way to gather settings dynamically",
    long_description=open('README.md').read(),
    install_requires=[
        "Django >=1.6 <=1.9",
    ],
    packages=['settings_composer']
)
