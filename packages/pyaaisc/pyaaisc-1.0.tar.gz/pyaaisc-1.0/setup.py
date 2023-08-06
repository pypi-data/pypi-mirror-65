import setuptools
import os


readme_dir = os.path.dirname(__file__)
readme_path = os.path.join(readme_dir, 'README.md')
with open(readme_path, "r") as f:
    long_description = f.read()


required_packages = [
    "beautifulsoup4",
    "requests"
]


setuptools.setup(
    name="pyaaisc",
    version="1.0",
    author="Stefan Stojanovic",
    author_email="stefs304@gmail.com",
    description="Python AAindex database scrape",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stefs304/pyaaisc",
    packages=[
        'pyaaisc',
    ],
    install_requires=required_packages,
    classifiers=(
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry"
    )
)
