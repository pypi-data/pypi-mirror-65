from setuptools import setup, find_packages

with open("./requirements.txt", "r") as f:
    required = f.read().splitlines()

setup(
    name="dspl",
    packages=["dspl"],
    version="0.0.10",
    include_package_data=True,
    install_requires=required,
    author="Nikita Varganov",
    author_email="nikita.varganov.ml@gmail.com",
    license="MIT",
    description="Library for using in DS-Platform",
    url="https://github.com/NV-27/dspl",
    download_url="https://github.com/NV-27/dspl/archive/0.0.10.tar.gz",
    keywords=["dspl", "ds_platform", "ds_template"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent"
    ]
)