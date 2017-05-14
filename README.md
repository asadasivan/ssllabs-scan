ssllabs-scan
============
# Introduction
This tool provides a commmand line interface for Qualys SSL Labs APIs to test multiple sites. Currently it can be used to test the SSL/TLS Protocols supported. It can also be used to tests for Ciphers supported. Multiple hostnames can be passed using a file. 
Note: The project uses some reference from ssllabsscanner project (author Jonathan C Trull).

## Getting Started
Checkout the project and start using it.

## Prerequisites
Python ~2.7

## Usage
python SSLScanner.py [options]
| Option  | Description |
| ------------- | ------------- |
|-f, --urlfile|File that contains list of host names or IP address|
|-p, --protocol|Test for SSL or TLS Protocols supported|
|-c, --cipher|Test for Ciphers supported|
|-o,--outputfile|File that contains the result of the test|


## Getting Help
contact Arunkumar Sadasivan <mailtosarun@gmail.com>

## Contributing
1. Fork it
2. Commit your changes 
3. Push to the branch
4. Create new Pull Request

## Issues
To report issues, bugs and enhancements requests, use the issue tracker. 


