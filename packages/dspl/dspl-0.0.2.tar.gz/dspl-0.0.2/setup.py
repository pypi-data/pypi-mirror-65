from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

with open("README.md") as f:
    readme = f.read()

setup(
    name="dspl",
    packages=["dspl"],
    version="0.0.2",
    install_required=required,
    zip_safe=True,
    author="Nikita Varganov",
    author_email="nikita.varganov.ml@gmail.com",
    license="MIT",
    description="Library for using in DS-Platform",
    url="https://github.com/NV-27/dspl",
    download_url="https://github.com/NV-27/dspl/archive/0.0.2.tar.gz",
    keywords=["dspl", "ds_platform", "ds_template"],
    ling_description=readme,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent"
    ]
)