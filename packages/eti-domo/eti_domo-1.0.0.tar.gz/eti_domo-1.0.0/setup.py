import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eti_domo", # Replace with your own username
    version="1.0.0",
    author="Andrea Michielan",
    author_email="michielan8@gmail.com",
    description="An interface to the REST API of a Came Eti/Domo server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrea-michielan/eti_domo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
    python_requires='>=3.6',
)