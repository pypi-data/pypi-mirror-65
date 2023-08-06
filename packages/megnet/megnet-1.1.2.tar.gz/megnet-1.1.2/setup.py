from setuptools import setup
from setuptools import find_packages
import os

this_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='megnet',
    version='1.1.2',
    description='MatErials Graph Networks for machine learning of molecules and crystals.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Chi Chen',
    author_email='chc273@eng.ucsd.edu',
    download_url='https://github.com/materialsvirtuallab/megnet',
    license='BSD',
    install_requires=['keras>=2.3.0', 'numpy', "scikit-learn",
                      'pymatgen>=2019.10.4', 'monty'],
    extras_require={
        'model_saving': ['h5py'],
        'molecules': ['openbabel', 'rdkit'],
        'tensorflow': ['tensorflow>=2'],
        'tensorflow with gpu': ['tensorflow-gpu>=2'],
    },
    packages=find_packages(),
    package_data={
        "megnet": ["*.json", "*.md"],
        "mvl_models": ["*/*.json", "*/*.md", "*/*.hdf5"],
    },
    keywords=["materials", "science", "machine", "learning", "deep", "graph", "networks", "neural"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    entry_points={
        'console_scripts': [
            'meg = megnet.cli.meg:main',
        ]
    }
)
