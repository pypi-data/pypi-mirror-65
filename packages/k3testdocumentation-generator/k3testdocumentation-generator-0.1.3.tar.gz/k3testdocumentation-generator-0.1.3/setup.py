from setuptools import setup, find_packages
import re

def get_version():
    with open("k3testdocumentation_generator/_version.py") as fh:
        verLine = fh.read()
        m = re.match("\s*__version__ *= *[\"']([\d.]+)[\"']", verLine)
        if m:
            return m.group(1)
        else:
            raise RuntimeError("Unable to determine version of the project")

def get_long_description():
    with open("README.md", "r") as fh:
        return fh.read()


setup(
    name='k3testdocumentation-generator',
    version=get_version(),
    
#     # project description parameters. These should be filled in accordingly
    author="Joachim Kestner",
    author_email="joachim.kester@khoch3.de",
    description="Tool for generating test documentation",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    python_requires='~=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    
    # packages for distribution are found & included automatically
    packages=find_packages(exclude=["tests.*", "tests", "example_test_dir", "example_test_dir*", "venv", "venv*"]),
    # for defining other resource files if they need to be included in the installation
    package_data={
        '' : ['*.md', '*.html']
    },
    
    # Set this is using a MANIFEST.in 
    # include_package_data=True,
    
    # libraries from PyPI that this project depends on
    install_requires=[
        "k3logging==0.1",
        "Jinja2",
        #"FPDF",
        "pdfkit",
        "markdown"
    ],
    entry_points={
        'console_scripts': [
            # a list of strings of format:
            # <command> = <package>:<function>
            'k3testdocumentation-generator = k3testdocumentation_generator.main.cli:main'
            # , ...
        ]
    }
)