import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="barry",
    version="0.0.1",
    author="Fabian Zoepf",
    author_email="zoepf.fabian@gmail.com",
    description="Bar plots in terminal window",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fabianzoepf/barry",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)