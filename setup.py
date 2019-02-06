import setuptools

with open("README.md", 'r') as readme:
    long_desc = readme.read()

setuptools.setup(
    name="pycolims",
    version="0.2.0",
    author="Daniel Paz Avalos",
    author_email="dpazavalos@protonmail.com",
    description="An importable, single stage CLI menu package",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/dpazavalos/pycolims",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3.7",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent"],
)
