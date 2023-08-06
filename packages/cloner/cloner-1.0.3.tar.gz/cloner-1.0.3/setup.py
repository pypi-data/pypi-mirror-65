import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloner",
    version="1.0.3",
    author="Ari Kardasis",
    author_email="ari.kardasis@gmail.com",
    description='A tiny utility for cloning github repos',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kardasis/cloner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    py_modules=['cloner'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        cloner=cloner.cli:cli
    '''
)
