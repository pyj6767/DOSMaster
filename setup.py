from setuptools import find_packages, setup

from main import __version__

# with open("README.rst") as file:
#     long_description = file.read()

setup(
    name="dosmaster",
    version=__version__,
    description="DOS(Density Of States) Plot Smartly",
    url="https://github.com/pyj6767/DOSMaster",
    author="Youngjun Park, Jaeson Kim",
    author_email="yjpark29@postech.ac.kr",
    #long_description=long_description,
    license="CNMD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    keywords="vasp dos",
    packages=find_packages(),
    python_requires=">=3.7.13",
    install_requires=[
        "numpy",
        "matplotlib",
        "pandas>=1.3.5",
        "ase>=3.22.1",
    ],
    # package_data={ #python 파일이 아닌 다른 파일들을 포함시키는 옵션
    #     "dosmaster": [
    #         "symmetry/bradcrack.json",
    #         "plotting/orbital_colours.conf",
    #         "plotting/sumo_base.mplstyle",
    #         "plotting/sumo_bs.mplstyle",
    #         "plotting/sumo_dos.mplstyle",
    #         "plotting/sumo_optics.mplstyle",
    #         "plotting/sumo_phonon.mplstyle",
    #     ]
    # },
    #data_files=["examples/orbital_colours.conf", "LICENSE"],
    entry_points={
        "console_scripts": [
            "dosmaster = main.dosmaster:main", #main : 폴더, dosmaster : python 파일, main : 함수
        ]
    },
)
