# from setuptools import setup
#
# setup(
#     name='undmainchain',
#     packages=['undjmainchain'],
#     version='0.0.3',
#     # Start with a small number and increase it with every change you make
#     license='MIT',
#     # Chose a license from here: https://help.github.com/articles/licensing-a-repository
#     description='Helper tools for administering the Unification Mainchain',
#     # Give a short description about your library
#     author='Indika',  # Type in your name
#     author_email='indika@unification.com',  # Type in your E-Mail
#     url='https://github.com/unification-com/mainchain-helpers',
#     # Provide either the link to your github or to your website
#     download_url='https://github.com/unification-com/mainchain-helpers/archive/v_01.tar.gz',
#     keywords=['undmainchain'],
#     # Keywords that define your package best
#     install_requires=[  # I get to this in a second
#         'click',
#         'requests',
#     ],
#     classifiers=[
#         'Development Status :: 3 - Alpha',
#         # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
#         'Intended Audience :: Developers',
#         # Define that your audience are developers
#         'Topic :: Software Development :: Build Tools',
#         'License :: OSI Approved :: MIT License',  # Again, pick a license
#         'Programming Language :: Python :: 3',
#         # Specify which pyhton versions that you want to support
#         'Programming Language :: Python :: 3.4',
#         'Programming Language :: Python :: 3.5',
#         'Programming Language :: Python :: 3.6',
#     ],
# )

import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

requires = [
    'click>=6.7',
]

setuptools.setup(
    name="undmainchain",
    packages=['undmainchain'],
    version="0.0.4",
    author="Unification Foundation",
    author_email="indika@unification.com",
    description="Helper tools for administering the Unification Mainchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/unification-com/mainchain-helpers",
    include_package_data=True,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
