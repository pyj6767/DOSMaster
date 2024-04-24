from setuptools import find_packages, setup

from dosmaster.main import __version__

#with open("README.md") as file:
#    long_description = file.read()

setup(
    name="dosmaster",
    version=__version__,
    description="DOS(Density Of States) Plot Smartly in Terminal",
    url="https://github.com/pyj6767/DOSMaster",
    author="Youngjun Park, Jaeson Kim in CNMD",
    author_email="yjpark29@postech.ac.kr",
    #long_description=long_description,
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="vasp dos",
    packages=find_packages(),
    python_requires=">=3.7.13",
    install_requires=[
        "numpy",
        "matplotlib",
        "pandas>=1.3.5",
        "ase>=3.22.1",
        "colorama>=0.4.6",
        "PyYAML",
    ],
    package_data={
        "dosmaster": [
            "dosmaster/subplotter/colors.csv",
        ]
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "dosmaster = dosmaster.main.dosmaster:main",
        ]
    },
)
