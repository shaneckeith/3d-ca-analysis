from setuptools import setup, find_packages

setup(
    name="3d-ca-analysis",
    version="1.0.0",
    author="Shane Keith",
    description="3D Low-Count Totalistic Cellular Automata Analysis",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "pandas",
    ],
    python_requires=">=3.8",
)
