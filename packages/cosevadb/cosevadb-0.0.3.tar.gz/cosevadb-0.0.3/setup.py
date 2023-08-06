import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cosevadb", # Replace with your own username
    version="0.0.3",
    author="Prakash Maria Liju P",
    author_email="ppml38@gmail.com",
    description="Light weight SQL database designed to manage data in csv format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ppml38/cosevadb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
