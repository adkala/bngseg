from setuptools import setup

setup(
    name='bngseg',
    version='1.0',
    description='Utility functions for lane segmentation data collection via BeamNG from existing map',
    author='Addison Kalanther',
    author_email='addikala@berkeley.edu',
    packages=['bngseg'],
    install_requires=['beamngpy']
)