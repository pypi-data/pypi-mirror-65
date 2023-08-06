"""
@author: Alejandro Cuartas
"""
from fxsim import optimizer
from setuptools import  setup, find_packages

setup(
    name="fxsim",
    version="0.0.24",
    description="Simulador de operacion en mercado forex",
    author="Alejandro Cuartas",
    author_email="alejandro.cuartas@yahoo.com",
    url="http://www.alejandrocuartas.com/",
    packages= find_packages(),
    license="MIT",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]

)