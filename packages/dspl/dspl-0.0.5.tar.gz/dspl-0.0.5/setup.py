import os
import os.path
from setuptools import setup, find_packages

def find_requires():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    requirements = []
    with open("{0}/requirements.txt".format(dir_path), "r") as reqs:
        requirements = reqs.readlines()
    return requirements    

setup(
    name="dspl",
    packages=["dspl"],
    version="0.0.5",
    include_package_data=True,
    install_requires=find_requires(),
    author="Nikita Varganov",
    author_email="nikita.varganov.ml@gmail.com",
    license="MIT",
    description="Library for using in DS-Platform",
    url="https://github.com/NV-27/dspl",
    download_url="https://github.com/NV-27/dspl/archive/0.0.5.tar.gz",
    keywords=["dspl", "ds_platform", "ds_template"],
    #long_description=readme,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent"
    ]
)