import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cldpy",
    version="0.0.14",
    author="cloudpy.io",
    author_email="author@example.com",
    description="cloudpy.io",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ortutay/cldpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    # TODO: review these dependencies, see which can be removed
    install_requires=[
        'numpy>=1.15.4',
        'pandas>=0.23.4',
        'cloudpickle>=0.6.1',
        'humanize>=2.2.0',
        'requests>=2.20.0',
        'requests-toolbelt>=0.8.0',
    ],
)
