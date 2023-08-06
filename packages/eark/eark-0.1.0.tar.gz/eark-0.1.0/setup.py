"""Setup file
"""

import setuptools

import eark

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='eark',
                 version=eark.__version__,
                 description='Emulating Astronautical Reactor Kinetics',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url=eark.__github_url__,
                 author='Vigneshwar Manickam',
                 author_email='vigneshwar.manickam@gatech.edu',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 zip_safe=False)
