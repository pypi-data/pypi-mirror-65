import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyeasydriver",
    version="0.0.1",
    author="Ishaat Chowdhury",
    author_email="ishaat@ualberta.ca",
    description="Driver for stepper motors controlled by SparkFun EasyDriver board",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ECE-492-W2020-Group-6/pyeasydriver",
    packages=setuptools.find_packages(exclude=("tests",)),
    license="MIT",
    install_requires=[
        "gpiozero>=1.5.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
