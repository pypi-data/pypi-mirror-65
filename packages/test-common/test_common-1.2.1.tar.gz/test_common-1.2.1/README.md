[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Travis (.org)](https://img.shields.io/travis/dante-signal31/test_common_python)](https://travis-ci.com/dante-signal31/test_common_python)
![Codecov](https://img.shields.io/codecov/c/github/dante-signal31/test_common_python)
[![GitHub issues](https://img.shields.io/github/issues/dante-signal31/test_common_python)](https://github.com/dante-signal31/test_common_python/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/dante-signal31/test_common_python)](https://github.com/dante-signal31/test_common_python/commits/master)
# test_common
Common functions useful for tests.
____

In this package you can find some functions I use frequently at my tests.

## Modules list
### benchmark
Package with modules to measure apps performance.
###### timing
Functions to take time related features. 
### fs 
Package with filesystem utilities. They are useful to prepare folders and files for your tests.
###### crypto
Cryptographic functions for your tests. Here you can find hashing functions to check file contents.
###### ops
Functions for file operations (copy, delete, etc).
### random 
Utilities to generate random content for your tests. Includes next modules:
###### crypto
Functions to create random strings.
### system
Utilities to deal with your hot operating system. Includes next modules:
###### env
Functions to manipulate environment variables