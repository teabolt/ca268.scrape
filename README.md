# ca268.scrape
A web scraper and a script for retrieving student programs and lecturer's descriptions from an internal programming website "Poodle" (module CA268).
The website contains hierarchical nested content. Main use case for this is archiving.

The Python third-party web scraping framework ```scrapy``` is used for the purpose, as well as built-in Python libraries.

Note that this scrapes HTML views, so the scraper can break any time the website changes.


## Requirements
* Python 3
* Scrapy 1.5.1

## Video showcase

<a href="https://youtu.be/nFgYS49q0Y4" target="_blank"><img src="http://img.youtube.com/vi/nFgYS49q0Y4/0.jpg" alt="Image from video showing the command-line and the file explorer" width="240" height="180" border="10" /></a>


## Usage (command line)

(Use the path separator and python invokation appropriate for your Operating System. The examples here show Windows)

### Web scraper: Sends requests to the web server and processes the responses.

```
cd <project_directory>/poodle_scrp
scrapy crawl ca268
```

* Enter username and password for the website before the scraper can continue.
* Find results (jsonlines files) in a directory with the current datetime

### Output organiser: Extracts JSONLines to human-readable appropriate files, under suitable directories.

```
cd <project_directory>
py -3.7 orgout.py <input_directory_path> [output_directory_path]
```

* Directory paths support relative path notation.
* Output directory is optional. If it is not provided, a directory is made alongside 'input_directory'.
* Find new directories, .txt, and .py files under the output directory.


## Implementation
The relevant source code is:
* ```poodle_scrp\poodle_scrp```
  * ```spiders\ca268.py```
    * ```Log in functionality, requests, response processing, data output```
  * ```pipelines.py```
    * item exporter class ```DataTypeJsonLinesExporter```, writes dict output to appropriate jsonlines file
  * ```settings.py```
    * activates the custom pipeline
* ```orgout.py```
  * class ```Ca268Organiser```, completely dependent on the format of the scraper's output lines

## Other

### More specific system requirements

The code was tested with:
* python 3.7.2 32-bit Windows
* pip freeze (for project's venv):
```
asn1crypto==0.24.0
attrs==18.2.0
Automat==0.7.0
cffi==1.11.5
constantly==15.1.0
cryptography==2.4.2
cssselect==1.0.3
hyperlink==18.0.0
idna==2.8
incremental==17.5.0
lxml==4.3.0
parsel==1.5.1
pyasn1==0.4.5
pyasn1-modules==0.2.3
pycparser==2.19
PyDispatcher==2.0.5
PyHamcrest==1.9.0
pyOpenSSL==18.0.0
pypiwin32==223
pywin32==224
queuelib==1.5.0
Scrapy==1.5.1
service-identity==18.1.0
six==1.12.0
Twisted==18.9.0
w3lib==1.20.0
zope.interface==4.6.0
```

### Future enhancements / points
* Give choice to the user regarding file/directory names, other text.
* Improve scraper output (nice documented fields, relationships to other items).
* Multiple export formats not just JSONLines.
* Scrapy features: caching, item pipelines, item classes.
