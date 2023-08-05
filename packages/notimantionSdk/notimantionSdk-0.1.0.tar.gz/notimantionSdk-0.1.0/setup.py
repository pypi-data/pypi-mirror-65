import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="notimantionSdk",
    version="0.1.0",
    author="Gustavo Ghioldi",
    author_email="gustavoghioldi@gmail.com",
    description="Sdk notimation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gustavoghioldi/ghistylus",
    packages=setuptools.find_packages(),
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'requests',
      ],
)