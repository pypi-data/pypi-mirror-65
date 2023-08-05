import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [line.rstrip('\n') for line in open("etl_pbshop/requirements.txt")]

setuptools.setup(
    name="etl-pbshop",
    version="0.0.7",
    author="Daniel S. Camargo",
    author_email="daniel.camargo@portobelloshop.com.br",
    description="Create your ETL integrations easy and quickly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/inovacaodigital/etl_pbshop_lib",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
