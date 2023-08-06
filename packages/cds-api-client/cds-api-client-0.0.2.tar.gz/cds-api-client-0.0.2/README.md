
# cds-api-client  0.0.2

A Python client package for accessing data from an API that follows the [Consumer Data Standards](https://github.com/stephenmccalman/cds-python-api-client/tree/0.0.2#api-documentation-pages) (CDS).

You are welcome to install and use this Python package. But before doing so:

* read the '[About this package](https://github.com/stephenmccalman/cds-python-api-client/tree/0.0.2#about-this-package)' section of this README page;
* consult the [documentation pages](https://github.com/stephenmccalman/cds-python-api-client/tree/0.0.2#api-documentation-pages) of each API provider for the availability of their endpoint paths and data resources; and
* review this package's [license](https://github.com/stephenmccalman/cds-python-api-client/blob/0.0.2/LICENSE).

Also, bear in mind that this package is NOT part of the official Consumer Data Standards' project nor any API implementation of the Standards.

## Requirements

Python 3.4+

## Installation

### From the package's [PYPI](https://pypi.org/project/cds-api-client) repository:

To install the latest version:

```sh
pip install cds-api-client --user
```

To install this specific version of the package:    
    
```sh
pip install cds-api-client=0.0.2 --user
```
    
### From the package's [Github](https://github.com/stephenmccalman/cds-python-api-client.git) repository:

To install the latest version:

```sh
pip install git+https://github.com/stephenmccalman/cds-python-api-client.git --user
```

To install this specific version of the package:

```sh
pip install git+https://github.com/stephenmccalman/cds-python-api-client.git@0.0.2 --user
```

## Import statement

To import the package:

```python
import cds
```

## Basic Usage

To access (banking) products data from a bank API that follows the Consumer Data Standards:

```python
import cds
from cds.rest import ApiException
from pprint import pprint

configuration = cds.Configuration()
configuration.host = 'https://data.holder.com.au' + '/cds-au/v1'  
api_client = cds.ApiClient(configuration)

products_api = cds.ProductsApi(api_client)

try:
    products_list = products_api.list_products(x_v='1')  # use x_v='2' from August 2020
except ApiException as e:
    print(e)
    
pprint(products_list.data)
```

Replace `https://data.holder.com.au` with the API host address of a bank.

## About this package

I generated this package with an open-source Java commandline interface (CLI) tool (swagger-codegen-cli-2.4.12.jar) that I downloaded from the [Swagger Codegen Project](https://github.com/swagger-api/swagger-codegen/#generators)'s [Maven repository](https://repo1.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.12/). 
                                                                                                                                                     
The Swagger-Codegen CLI generates an API client package from a Swagger specification file -- a JSON- (or YAML-) formatted text file that lists the endpoint paths and data definitions of an API, or a group of APIs.  

To generate this package, I used a Swagger specification file of the Consumer Data Standards (1.2.0), which I downloaded from the Standards' [Github page](https://consumerdatastandardsaustralia.github.io/standards); you can find a copy of the file (cds_full.json) in the [.swagger-codegen](https://github.com/stephenmccalman/cds-python-api-client/tree/0.0.2/.swagger-codegen/) directory of the package.

The Swagger-Codegen CLI generates the package's files from a set of templates that it fills with information it retrieves from the specification file. The  CLI comes with a set of generic templates built in. 

Before generating this package, I extracted these built-in templates from the CLI and modified them to better document the package, and remove redundant code; you can find the templates that I used to generate the package in the [.swagger-codegen/templates](https://github.com/stephenmccalman/cds-python-api-client/tree/0.0.2/.swagger-codegen/templates) directory.  
           
If you're interested in generating this package (or a modified version of it), have a look at this [makefile](https://github.com/stephenmccalman/cds-python-api-client/blob/0.0.2/.swagger-codegen/makefile) that I created. The makefile contains a receipe for making the package.  You can find this makefile and instructions on how to use it in the [.swagger-codegen]([.swagger-codegen/templates](https://github.com/stephenmccalman/cds-python-api-client/tree/0.0.2/.swagger-codegen) directory. 

## What is (and isn't) in this package

This Python package contains:
- a module (`.py`) file for each endpoint path and each data definition (that is listed in the specification file); and
- a number of supporting files:
    - the primary package files: configuration.py, api_client.py, rest.py, and the init.py files; and
    - the project files: this README.md, setup.py, requirements.txt, .gitignore and .swagger-codegen-ignore.
    
All of these files are generated by the CLI.  The CLI (under default settings) can also generate a documentation (markdown) page and a test module for each endpoint path and each data definition. It can also generate a number of other project files, like a test-requirements.txt and a tox.ini (among other files). For simplicity, this package does not include these extra files. 


##  The Consumer Data Standards

The [Consumer Data Standards](https://consumerdatastandardsaustralia.github.io/standards) are a set of technical standards for implementing the Australian Government's  [Consumer Data Right](https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_Search_Results/Result?bId=r6370) (CDR) legislation. The CDR aims to help consumers, whether they be an individual, household or a small business, find better deals on retail products and services, by

* giving them greater control over their own customer data, and 
* assisting them to compare retail products and services across businesses.

The CDR requires a business to
* provide their customers access to their own customer data -- namely account and transaction data;
* publish specific data on retail products and services that the business offers;
* make (both types of) data available in a standard format and through a standard process (that is set out by a Data Standards Body appointed by the Australian Government); and
* allow individual consumers to permit a trusted third party to access their customer data on their behalf.

The Australian Government is rolling out the CDR on a sector-by-sector basis, beginning in the banking sector. It appointed the [ACCC](https://www.accc.gov.au/focus-areas/consumer-data-right-cdr-0) to regulate the CDR and its roll out. In short, the ACCC determines which, and when, data fall under the CDR regime, and which third parties can access the data on behalf of a consumer.

The Government also appointed (the CSIRO's) [Data61](https://consumerdatastandards.org.au/) as the Data Standards Body. As the DSB, Data61 maintains as set of technical standards called the Consumer Data Standards. The Consumer Data Standards (among other things) set out the digital formats and processes  by which businesses must make available "designated" data to consumers and "accredited" third parties.

## API documentation pages

Below lists the links to API documentation pages of the four major Australian banks:

* [Commonwealth Bank of Australia (CBA)](https://www.commbank.com.au/Developer/)
* [National Australia Bank (NAB)](https://developer.nab.com.au/products)
* [Australia and New Zealand (ANZ) Banking Group](https://www.anz.com.au/support/anz-apis/)
* [Westpac Banking Corporation (WBC)](https://www.westpac.com.au/about-westpac/innovation/open-banking/)

## License

BSD 3-Clause License

Copyright (c) 2020, Stephen McCalman
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
