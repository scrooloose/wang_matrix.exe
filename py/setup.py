from setuptools import find_packages, setup

setup(
    name="wangmatrix",
    version="0.0.0",
    description="Marty and Rich solve mazes",
    author="Richard Wall",
    url="https://github.com/scrooloose/wang_matrix.exe",
    license="",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "attr",
        "zope.interface",
    ],
    extras_require={
        "dev": [
        ],
    },
    entry_points={
        "console_scripts": [
            "wangmatrix.solve.py = wangmatrix.solver:main",
            "wangmatrix.generate.py = wangmatrix.generate:main",
            "wangmatrix.bsp.py = wangmatrix.bsp:main",
        ],
    },
)
