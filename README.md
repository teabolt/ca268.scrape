## Update

This has been renamed from 'ca268.scrape' to 'poodle.scrape'. The "Poodle" website is used to run multiple courses, including Data Structures and Algorithms (ca268) during first (Fall) semester and Object Oriented Programming (ca269) during second (Spring) semester. This program can now scrape from both courses (initially it only supported 'ca268').

# poodle.scrape

A <a href="https://www.python.org/">Python</a> program for downloading students' uploaded code and lecturer's task descriptions from the internal (log-in required) website "Poodle", a website used in <a href="https://www.dcu.ie/">Dublin City University</a> for programming courses.

Done for learning purposes only. This project shows a web scraper built using the ```scrapy``` Python framework for retrieving hierarchical, nested content. The main use for this is in letting a student archive their work.

Note that this scrapes HTML views, so the scraper can break any time the "Poodle" website changes.

## Requirements
* <a href="https://www.python.org/downloads/">Python 3</a>
* <a href="https://scrapy.org/">Scrapy</a>

## Installation
```
git clone https://github.com/teabolt/poodle.scrape.git
cd poodle.scrape
pip install -r requirements.txt
```

## Usage (command line)

### Run the scraper (download student and lecturer's data from "Poodle")

In the following usage examples, angle brackets (<>) indicate a required argument. Square brackets ([]) indicate an optional argument. Do not include the brackets when passing the argument.

```
python run.py <course-code> [save-dir]
```
* ```course-code``` is either 'ca268' (for data structures and algorithms) or 'ca269' (for object oriented programming).
* ```save-dir``` is a path to the directory where scraped items should be saved. Defaults to the current date and time.

* Enter your Poodle username and password so that the scraper can continue (this is for authentication purposes only).
* Find the results in the directory specified as .jsonlines files.

Alternatively, instead of using the ```run.py``` script you can use the scrapy command line tool:

```scrapy crawl poodler -a course=<course-code> [-a save_dir=<save-dir>]```


### Organise the output (make the downloaded content nice to read)

```
python orgout.py <input-dir> [output-dir]
```
* ```input-dir``` is a path to the directory with scraped items, to be organised.
* ```output-dir``` is a path to the directory where the organised items are to be written to. Defaults to ```input-dir``` with ```_organised``` appended to the directory name.

* Find the results in ```output-dir```, including subdirectories, .txt, and .py files.

## Linux video showcase, Python 3.7.3 64-bit Ubuntu 18.04 LTS



## Windows video showcase, Python 3.7.2 64-bit Windows

<a href="https://youtu.be/nFgYS49q0Y4" target="_blank"><img src="http://img.youtube.com/vi/nFgYS49q0Y4/0.jpg" alt="Image from video showing the command-line and the file explorer" width="240" height="180" border="10" /></a>


## Implementation details

### The project consists of two components:
1. Web scraper: Sends requests to the web server and processes the responses. Includes the "poodler" spider.
2. Output organiser: Extracts JSONLines to human-readable and source code files, under suitable directories.

### The relevant project files are:
* ```run.py```
  * python CLI to the crawler.
* ```orgout.py```
  * class ```Ca268Organiser```, sorts and writes scraped items, dependent on spider's output.
* ```utils.py```
  * datetime, string functions.
* ```scrapy.cfg```
  * Scrapy project settings (auto-generated).
* ```/poodle_scrp```
  * ```spiders/poodler.py```
    * Log in functionality, requests for task pages, parsing out items into dicts.
  * ```pipelines.py```
    * item exporter class ```DataTypeJsonLinesExporter```, converts dicts to jsonlines, writes files.
  * ```settings.py```
    * activates the custom item exporter pipeline
    * enables request caching


### Log-in functionality:
The course page is requested. A form is filled out.


### Terminology used throughout the spider's source code:
* VPL (Virtual Programming Lab): A single programming task for which the student may be required to submit some source code.
* Section: A collection of related VPL's centered on a single topic, during a certain week in college, i.e. binary trees, generics.
* Submission view: Part of VPL where student source code is uploaded / shown.


### Design decisions:
* JSONLines is used over JSON for scalability and simplicity ("flat is better than nested").


### Future enhancements
* Improve scraper output (nice documented fields, relationships to other items).
* Support multiple export formats, not just JSONLines.
* Use more scrapy features: item pipelines, item classes.
* Integrate ```run.py``` and ```orgout.py``` to execute them together with one command.
* Refactor ```orgout.py```. It is very coupled to the web scraper's output. It could be removed with functionality moved to other modules.


### Known issues
* Grabbing a VPL with multiple submission files only grabs the first submitted file, not fetching other files.