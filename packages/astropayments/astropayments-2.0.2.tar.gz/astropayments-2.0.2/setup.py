import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="astropayments", 
    version="2.0.2",
    author="astropayments",
    author_email="integrations@goastro.com",
    description="sdk for astropayments rest api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://api.goastro.com/",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)