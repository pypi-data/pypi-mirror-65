import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gym-cap32", # Replace with your own username
    version="1.0.1",
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
