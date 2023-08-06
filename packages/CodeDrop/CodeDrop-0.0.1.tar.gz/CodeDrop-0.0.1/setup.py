import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='CodeDrop',
    version="0.0.1",
    author="Pritom Sarker",
    author_email="pritoms@gmail.com",
    description='Upload python files directly from your script to dropbox.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pritoms/CodeDrop",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)