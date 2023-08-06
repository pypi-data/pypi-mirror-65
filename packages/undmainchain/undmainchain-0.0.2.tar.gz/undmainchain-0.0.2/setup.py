import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


requires = [
    'click>=6.7',
]

setuptools.setup(
    name="undmainchain",
    version="0.0.2",
    author="Unification Foundation",
    author_email="indika@unification.com",
    description="Helper tools for administering the Unification Mainchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/unification-com/mainchain-helpers",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
