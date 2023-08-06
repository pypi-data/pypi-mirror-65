import setuptools
from pathlib import Path

p = Path(__file__).parents[0]

P_README = p / "README.md"
with open(P_README, "r") as f:
    LONG_DESCRIPTION = f.read()

P_VERSION = p / "VERSION"
with open("VERSION", "r") as f:
    VERSION = f.read()

setuptools.setup(
    name="pixhist",
    version=VERSION,
    author="Sidney Radcliffe",
    author_email="sidneyradcliffe@gmail.com",
    description="Pixel histograms.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/sradc/PixHist",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["numpy", "numba"],
    extras_require={
        'pixhist.rendering':  ["matplotlib"]
    },
)
