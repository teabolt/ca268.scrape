## Update

This has been renamed from 'ca268.scrape' to 'poodle.scrape'. The "Poodle" website is used to run multiple courses, including Data Structures and Algorithms (ca268) during first (Fall) semester and Object Oriented Programming (ca269) during second (Spring) semester. This program can now scrape from both courses.

# poodle.scrape

A <a href="https://www.python.org/">Python</a> program for downloading students' uploaded code and lecturer's task descriptions from the internal (log-in required) website "Poodle", a website used in <a href="https://www.dcu.ie/">Dublin City University</a> for programming courses.

Done for learning purposes only. This project shows a web scraper built using the ```scrapy``` Python framework for retrieving hierarchical, nested content. The main use for this is in letting a student archive their work.

Note that this scrapes HTML views, so the scraper can break any time the "Poodle" website changes.

## Requirements
* <a href="https://www.python.org/downloads/">Python 3</a>
* <a href="https://scrapy.org/">Scrapy</a>

## Installation
* ```git clone ```
* ```cd poodle.scrape```
* ```pip install -r requirements.txt```


## Usage (command line)

(Use the path separator and python invokation appropriate for your Operating System. The examples here show Windows)

### Web scraper: Sends requests to the web server and processes the responses.

```
cd <project_directory>/poodle_scrp
scrapy crawl ca268
```

* Enter username and password for the website before the scraper can continue.
* Find results (jsonlines files) in a directory with the current datetime

### Alternative: use run.py

### Output organiser: Extracts JSONLines to human-readable and source code files, under suitable directories.

```
cd <project_directory>
py -3.7 orgout.py <input_directory_path> [output_directory_path]
```

* Directory paths support relative path notation.
* Output directory is optional. If it is not provided, a directory is made alongside 'input_directory'.
* Find new directories, .txt, and .py files under the output directory.

## Linux video showcase, python 3.7.3 64-bit Ubuntu 18.04 LTS


## Windows video showcase, python 3.7.2 64-bit Windows

<a href="https://youtu.be/nFgYS49q0Y4" target="_blank"><img src="http://img.youtube.com/vi/nFgYS49q0Y4/0.jpg" alt="Image from video showing the command-line and the file explorer" width="240" height="180" border="10" /></a>



## Implementation
The relevant source code is in:
* ```poodle_scrp\poodle_scrp```
  * ```spiders\ca268.py```
    * Log in functionality, requests, response processing, data output
  * ```pipelines.py```
    * item exporter class ```DataTypeJsonLinesExporter```, writes dict output to appropriate jsonlines file
  * ```settings.py```
    * activates the custom pipeline
    * enables request caching
* ```run.py```
* ```orgout.py```
  * class ```Ca268Organiser```, dependent on the format of the scraper's output lines

## Other


### Future enhancements
* Improve scraper output (nice documented fields, relationships to other items).
* Multiple export formats not just JSONLines.
* Scrapy features: item pipelines, item classes.
* Integrate run.py and orgout.py to execute them together with one command.


### Known issues
* Grabbing a VPL with multiple submission files only grabs the first submitted file, not fetching other files.