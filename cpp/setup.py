from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension("SynthExpr", ["SynthExpr.cpp"]),
]

setup(
    name="SynthExpr",
    version="0.0.1",
    author="Paulo Cavalcanti",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    package_data={"SynthExpr": ["*.pyi"]},
    include_package_data=True,
)
