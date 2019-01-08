# Python
All scripts has been written by me

## Asana_improvements_project
Add some functionallity to asana, as: add default followers based on project or custom fields, weekly reports, etc. Required Asana API [Python lib](https://github.com/Asana/python-asana)

## BOParse
FTP/SFTP downloader and specific parser for big files, prepares data for back office system

## Cleanup script
Python script for simple cleanup of directories, launching from Groovy script (Jenkinsfile)
Valid documentation also available inside [cleanup script](https://github.com/Sysa/Python/tree/master/Cleanup_script)

### Parameters of pipeline project:

#### Groovy script:
* **NodeForCleanup** - name (or label) of jenkins node (worker/slave) where need to perform a cleanup

* **PathForCleanup** - Full path to directory, which must be cleared from old files.Note: backslashes must be changed to commond slashes, and don't forget about closing slash in the end of the path
For example: path `C:\MangoClient\Application Files` should be changed to `C:/MangoClient/Application Files/`

* **kl** - Keep Last - N number of files (or folders), which must be alive after cleanup. Only N newest files will be in safe.

* **ttl** - Time To Live - count of days since today, files older than this counter will be removed

* **venv** - path for new python virtual environment, where script will be launched.
Note: backslashes must be escaped with backslashes (doubled backslashes in sum)
For example: path `C:\ci\python_venv` must be `C:\\ci\\python_venv`

* **python_exec_path** - path to python interpreter on the machine where cleanup should be performed.
Note: backslashes must be escaped with backslashes (doubled backslashes in sum)
For example: path `C:\Python36\python.exe` must be `C:\\Python36\\python.exe`

* **EmailToReport** - E-mails to which execution report should to go. Emails separates by newline.
	* Example:
	* a@a.com
	* b@b.net


#### Python script:
###### optional arguments:
*   **-h, --help**         show this help message and exit
*   **--path** PATH        path for cleanup, for example `//C:/Users/Alex/Downloads/`
*   **--ttl** TTL          Time To Live - count of days since today, files older
                     than this counter will be removed
*   **--kl** KL            Keep Last - N number of files, which must be alive after
                     cleanup. Only N newest files will be in safe
*   **--emails** EMAILS    E-mails to which execution report should to go.Emails
                     separates by comma `,` and passes in one string. Example:
                     a@a.com,b@b.ru,etc@etc.net
*   **--job_url JOB_URL**  Optional, generally set by Jenkins environment variable.

## Genie to Asana
Python adapter to connect Siebel DB (Genie) to Asana's API

No documentation, integration with legacy software and DB

## PC Settings Backuper
Simple script to archive and move files, with e-mail report

No documentation

## book_parse
Script to grab e-book from web-portal and export results in xml\html\pdf

No documentation