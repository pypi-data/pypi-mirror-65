import setuptools
import os

with open("README.rst", "r") as fh:
    long_description = fh.read()


with open ('requirements.txt', 'r') as file:
    install_requires = file.readlines()
install_requires = [x.strip() for x in install_requires]

setuptools.setup(
    name="pynomial",
    version="1.0.4",
    author="Silver Creek",
    author_email="austin.mcleod@silvercreeksoftware.com",
    description="pynomial",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Silver-Creek/pynomial.git",
    download_url="https://github.com/Silver-Creek/pynomial/archive/v0.1.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires = install_requires,
    zip_safe=False
)



# Release Steps
# Upgrade setuptools
# >>> python -m pip install --user --upgrade setuptools wheel
# Create the distribution files
# >>> python setup.py sdist bdist_wheel
# Install Twine
# >>> python -m pip install --user --upgrade twine
# Upload the package tp test PyPi
# python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* (e.g. https://test.pypi.org/project/pygeostat/1.0.0/)
# Install the uploaded packeg to test PyPi and test on an environment
# pip install -i https://test.pypi.org/simple/ pygeostat
# After testing the test version upload it to PyPi
# twine upload dist/*