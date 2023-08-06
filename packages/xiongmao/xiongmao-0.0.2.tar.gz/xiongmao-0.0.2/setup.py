import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xiongmao", # Replace with your own username
    version="0.0.2",
    author="Johnny Lichtenstein",
    author_email="johnlichtenstein@gmail.com",
    description="Binding Pandas functions to dataframe as methods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnlichtenstein/xiongmao",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
