import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rbtoolz", 
    version="1.0.1",
    author="Ross Bonallo",
    author_email="rossbonallo@gmail.com",
    description="Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rbonallo/rbtoolz",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'plotly'
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
