import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="physique", # Replace with your own username
    version="0.3",
    author="David THERINCOURT",
    author_email="dtherincourt@gmail.com",
    description="Librairie Python pour les sciences physiques",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/david-therincourt/physique",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
