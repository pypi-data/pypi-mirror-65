"""Setup configuration."""
import setuptools

with open("README.md", "r") as fh:
    LONG = fh.read()
setuptools.setup(
    name="queueman",
    version="0.3",
    author="Joakim Sorensen",
    author_email="hi@ludeeus.dev",
    description="",
    long_description=LONG,
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/queueman",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
