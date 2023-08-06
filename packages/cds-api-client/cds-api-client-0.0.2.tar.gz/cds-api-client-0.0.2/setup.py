# BSD 3-Clause "New" or "Revised" License (BSD-3-Clause) 
# Copyright (c) 2020 Stephen McCalman. All rights reserved.


from setuptools import setup, find_packages  # noqa: H301

with open("README.md", "r") as fh:
    long_description = fh.read()


REQUIRES = [
    "certifi>=2017.4.17",
    "python-dateutil>=2.1",
    "urllib3>=1.23"
]
    

setup(
    name="cds-api-client",
    version="0.0.2",
    description="A Python client package for accessing data from an API that follows the Consumer Data Standards (CDS).",
    url="https://github.com/stephenmccalman/cds-python-api-client",
    author="Stephen McCalman",
    author_email="cds-api-client@googlegroups.com",
    keywords=["Consumer Data Standards","Swagger"],
    license="BSD",
    install_requires=REQUIRES,
    packages=find_packages(),
    python_requires='~=3.4',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",       
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
]
)
