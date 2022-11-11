## NFL fantasy
- Takes a csv file of nfl stats from fantasy.nfl.com <br>
- Reads all of the rows and saves them <br>
- Adds all of them to an SQLite database <br>
- SQLite db is then accessed by html file <br>
- Displays all data. Can also search and sort

### How to run:
To install flask: ```pip3 install flask```<br>
OPTIONAL: create a virtual environment using ```python3 -m venv venv``` <br>
For macOS and linux: ```. venv/bin/activate``` <br>
For windows: ```. venv/Scripts/activate``` <br>

Then leave the directory to run it: ```cd ..``` <br>

Export the variables: <br>
```export FLASK_APP=nflfantasy```<br>
```export FLASK_DEBUG=DEV```<br>

For Windows:
```export FLASK_APP=nflfantasy```<br>
```export FLASK_ENV=dev```<br>

Initialise the database:
```flask init-db```<br>

Run csv reading script:
```python3 nflfantasy/fantasy.py nflfantasy/stat-sheets/csv/fantasy.csv``` <br>

Run the App:
```flask run```