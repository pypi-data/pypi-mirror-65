import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="caverimx-db", # Replace with your own username
    version="0.0.2",
    author="Alexis Betancourt",
    author_email="alexis@caveri.mx",
    description="A small file system based database package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/caverimx/caverimx-db.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)