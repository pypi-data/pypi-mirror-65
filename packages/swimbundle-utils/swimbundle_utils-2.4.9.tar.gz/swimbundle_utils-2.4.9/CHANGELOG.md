# CHANGELOG

## 2.4.9 - 2020-04-3
* Added a relative time format in querystring parser

## 2.4.8 - 2020-03-31
* add better substring generation for ioc parsing

## 2.4.7 - 2020-03-30
* dependency fix

## 2.4.6 - 2020-03-27
* Adding a python library not inculded in the swimlane container

## 2.4.4-5 - 2020-03-20
* fixing issue with the package setup

## 2.4.3 - 2020-03-20
* Fixed issue with unicode literals in python2.7

## 2.4.2 - 2020-03-19
* Added handling for punycode in URLs to the IOC parser

## 2.4.1 - 2020-03-16
* Removed debug code in previous release

## 2.4.0 - 2020-03-13
* Added an IOC parser and typer

## 2.3.3 - 2020-3-01
* Fixed python3 build

## 2.3.3 - 2020-3-01
* Added QueryStringParser for a standard way to parse querystrings

## 2.3.2 - 2020-2-24
* Added kwarg overwriting to asset_parser

## 2.3.1 - 2020-2-13
* Fixed an edgecase in the flattener due to very nested list data

## 2.3.0 - 2020-01-24
* Added ability to setup Swimlane Exceptions for rest status codes

## 2.2.0 - 2019-12-16
* Added more Exceptions to exception module
* Added the option to provide a port to asset_parser

## 2.1.2 - 2019-11-13
* in LinkHeadersPaginationEndpoint, pagination now ends when the key "next" is not in links

## 2.1.1 - 2019-10-18
* Added ignore_dt_format to ignore datetime formats in parsing

## 2.1.0 - 2019-09-20
* Backwards incompatible bugfixes in flattener
* Docs

## 2.0.0 - 2019-09-06
* Added helper for testconnection
* Added helper for attachments
* Added custom validator
* Mintor Flattener restructure and refactor
* Updated cleanxmltodict in Flattener
* Added optional input flag to InputChecker
* Added option to autoparse out datetime strings
* Added a keep_simple_lists param if stringify is set

## 1.2.3 - 2019-09-04
* Bumped validators to 0.14.0

## 1.2.2 - 2019-09-04
* Bumped dict-plus dependency to 0.1.1

## 1.2.1 - 2019-09-04
* Added Flattener().flatten() alias, do_flatten()
* Moved changelog to correct spot

## 1.2.0 - 2019-08-27
* Updated flattener to be consistent with Py2 & Py3, and previous versions
* Added helper submodule for asset parsing and input checking

## 1.1.8 - 2019-08-08
* Updated package to be consistent with Python3 and Python2
* Added CHANGELOG

## 1.1.7 - 2019-06-19

* Added useragent from PR
* Added Mixin Cleanup from PR
* Added polling

## 1.1.6 - 2019-06-18

* Minor cleanup and fixes
* PR-4 Fixes
* Added clean_xmltodict helper func

## 1.1.2 - 2018-10-24

* Initial Package Version Tracking
