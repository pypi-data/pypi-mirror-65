import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IDS_XS_TOOLS-UiS",
    version="0.3",
    author="Ole Christian Handegård",
    author_email="ole.hande98@gmail.com",
    description="Image functions for IDS XS camera",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prinsWindy/ABB-pucks",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyzbar',
        'opencv-python',
        'pyueye',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)