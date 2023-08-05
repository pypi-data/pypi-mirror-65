import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="gym-cap32", # Replace with your own username
    version="1.0.4",
    author="Theo De castro Pinto, Wilfried Augeard",
    author_email="decastrotheo960@gmail.com",
    description="Gym environment for Amstrad CPC.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
        "amle_py": ["snap/*.sna"]
    },
    include_package_data=True,
)
