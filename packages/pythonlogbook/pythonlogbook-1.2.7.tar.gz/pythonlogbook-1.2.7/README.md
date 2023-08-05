# Python Logbook
This program enables it's users to instantly make a logbook entry from the terminal. The program instantly creates folders that correspond to the date that each entry was published. Each file is named as date_time. If you want to see all logs at once, you can do such with combineLogs.py, which will concatenate all logs into one long logbook.

## Getting Started
This app can be installed with pip3
```
pip3 install pythonlogbook
```
or pip
```
pip install pythonlogbook
```
## Using the Command Line Interface
To create a new log, run: `newlog` in your terminal. To combine logs, run: `combinelogs`. To make a markdown file, run: `makelogmd` It's as easy as that!

### Setting up directory
As of right now, the only way to change the folder where the logs are stored is by editing the variable originalPath so that line 11 of logbook.py says `originalPath = r"folderLocation"`.

Once you set this up, you should be able to run the program through the terminal by running `python logbook.py` while in the folder that the file is in.

## Built with
* Python

## Author

* **Luke Weiler** - [lukew3](https://github.com/lukew3)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
