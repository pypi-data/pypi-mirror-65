import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doop-codes", # Replace with your own username
    version="0.0.1",
    author="doop",
    author_email="doopcodes@gmail.com",
    description="Search python snippets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.doop.codes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
    python_requires='>=2.4',
)