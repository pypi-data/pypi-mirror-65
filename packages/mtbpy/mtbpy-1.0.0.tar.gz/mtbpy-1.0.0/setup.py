import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mtbpy",
    version="1.0.0",
    author="Minitab, LLC",
    author_email="techsupport@minitab.com",
    description="Module for communicating with Minitab from Python scripts executed via the PYSC command.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://support.minitab.com/minitab/19/python-integration/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering"
    ],
    python_requires=">=3.6.1",
    install_requires=[
        "protobuf >= 3.8.0",
        "grpcio >= 1.26.0",
    ],
    extras_require={
        "develop": [
            "grpcio-tools"
        ]
    }
)
