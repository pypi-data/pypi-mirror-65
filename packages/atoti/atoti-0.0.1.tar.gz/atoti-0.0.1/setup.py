import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atoti",
    version="0.0.1",
    description="Design, explore and deploy efficient and flexible data models",
    author="Atoti",
    author_email="dev@atoti.io",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.atoti.io",
    project_urls={
        "Documentation": "https://docs.atoti.io",
        "Bug Tracker": "https://github.com/atoti/atoti/issues",
    },
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=["pandas", "pyarrow!=0.14.1", "pyyaml"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Free To Use But Restricted",
        "Operating System :: OS Independent",
        "Programming Language :: Java",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Typing :: Typed",
    ],
    keywords=["aggregation calculation chart data dataviz pivot-table visualization"],
)
