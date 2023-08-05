import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spectra3D",
    version="0.0.1.3.2",
    author="Ben Knight",
    author_email="bknight@i3drobotics.com",
    description="Adding spectrum data to 3D",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/i3drobotics/Spectra3D",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy','matplotlib','plyfile'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)