from setuptools import setup, find_packages
from os import listdir
from os.path import isfile, join

with open('requirements.txt', 'rt') as f:
    install_requires = [l.strip() for l in f.readlines()]

setup(
    name='fslgui',
    version='0.0.0.dev8',
    description='fslgui',
    url='https://git.fmrib.ox.ac.uk/fsl/fslgui',
    author='Taylor Hanayik',
    author_email='hanayik@gmail.com',
    license='Apache License Version 2.0',
    classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Scientific/Engineering :: Visualization'],

    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts' : [
            'bet_gui        = fsl.gui.scripts.Bet_gui:main',
            'flirt_gui        = fsl.gui.scripts.Flirt_gui:main'
        ]
    },
    package_data={
    'fsl': ['gui/icons/*.png'],
    },

    )
