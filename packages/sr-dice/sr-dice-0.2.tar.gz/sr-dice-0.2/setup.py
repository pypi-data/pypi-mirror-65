import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sr-dice",
    version="0.2",
    license='EUPL-1.2',
    author="Brolf",
    author_email="brolf@magheute.net",
    description="A simple dice simulator for Shadowrun",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/br-olf/sr-dice",
    keywords=['dice','pen and paper','RPG','Shadowrun'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
