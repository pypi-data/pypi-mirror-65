import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fp:
    install_requires = fp.read()

setuptools.setup(
    name="nalej-platformer",
    version="0.5.1",
    author="Rodrigo Núñez",
    author_email="rnunez@nalej.com",
    description="Nalej Platform automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nalej/nalej-platformer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    python_requires='>=3.7',
    entry_points='''
        [console_scripts]
        nalej-platformer=nalej_platformer.cli.main:run
    '''
)
