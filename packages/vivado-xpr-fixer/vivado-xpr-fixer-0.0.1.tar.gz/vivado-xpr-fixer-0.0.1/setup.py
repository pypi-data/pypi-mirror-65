import setuptools

with open("README.md", 'r') as file_handler:
    long_description  = file_handler.read()

setuptools.setup(
    name="vivado-xpr-fixer",
    version="0.0.1",
    author="Jessie Shehan",
    author_email="jps111@uclive.ac.nz",
    description="A script to fix Vivado absolute path issues when working with git.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    entry_points='''
        [console_scripts]
        vivado-xpr-fixer=vivado_xpr_fixer.vivado_xpr_fixer:main
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)