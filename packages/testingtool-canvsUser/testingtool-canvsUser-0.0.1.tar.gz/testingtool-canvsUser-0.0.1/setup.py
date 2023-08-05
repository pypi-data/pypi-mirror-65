import pathlib
import pkg_resources
import setuptools

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

with open("README.md", "r") as fh:
    long_description = fh.read()

# with open('requirements.txt') as f:
#     required = f.read().splitlines()

setuptools.setup(
    name="testingtool-canvsUser", # Replace with your own username
    version="0.0.1",
    author="Janet Huang",
    author_email="janet.huang@canvs.ai",
    description="A package for custom canvs analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbproductionsLTD/canvs_tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=install_requires
)