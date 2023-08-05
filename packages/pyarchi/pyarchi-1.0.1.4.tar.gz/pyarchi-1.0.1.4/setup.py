# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyarchi',
 'pyarchi.data_objects',
 'pyarchi.initial_detection',
 'pyarchi.masks_creation',
 'pyarchi.output_creation',
 'pyarchi.proof_concept',
 'pyarchi.routines',
 'pyarchi.star_track',
 'pyarchi.utils',
 'pyarchi.utils.data_export',
 'pyarchi.utils.factors_handler',
 'pyarchi.utils.image_processing',
 'pyarchi.utils.misc',
 'pyarchi.utils.noise_metrics',
 'pyarchi.utils.optimization']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.0,<5.0',
 'matplotlib>=3.1.2,<4.0.0',
 'opencv-python>=4.1.2,<5.0.0',
 'pyyaml>=5.3,<6.0',
 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'pyarchi',
    'version': '1.0.1.4',
    'description': "Photometry for CHEOPS's background stars",
    'long_description': "[![Documentation Status](https://readthedocs.org/projects/archi/badge/?version=latest)](https://archi.readthedocs.io/en/latest/?badge=latest)\n# ARCHI - An expansion to the CHEOPS mission official pipeline\n\nCHEOPS mission, one of ESA's mission has been launched in December 2019. \n\nThe official pipeline released for this mission only works for the\ntarget star, thus leaving a lot of information  left to explore. Furthermore, the presence of background stars in our images\ncan mimic astrophysical signals in the target star. \n\n\nWe felt that there was a need for a pipeline capable of analysing those stars and thus, built archi, a pipeline\nbuilt on top of the DRP, to analyse those stars. Archi has been tested with simulated data, showing proper behaviour.\nON the target star we found photometric precisions either equal or slightly better than the DRP. For the background stars we found photometric preicision 2 to 3 times higher than the target star.\n\n# How to install archi \n\nThe pipeline is written in Python3, and most features should work on all versions. However, so far, it was only tested on python 3.6, 3.7 and 3.8\n\nTo install, simply do :\n\n    pip install pyarchi\n\n# How to use the library \n\nA proper introduction to the library, alongside documentation of the multiple functions and interfaces can be found [here](https://archi.readthedocs.io/en/latest/)\n\n\n# Known Problems\n\n [1] The normalization routine fails if one of the stars is saturated; Since the images are normalized in relation to their brigthest point, the saturation of a star leads to us being unable to detect faint stars (under a given magnitude threshold)\n \n [2] There is no correction for cross-contamination between stars\n",
    'author': 'Kamuish',
    'author_email': 'amiguel@astro.up.pt',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kamuish/archi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
