## NFL fantasy
- Takes a csv file of nfl stats from fantasy.nfl.com <br>
- Reads all of the rows and saves them <br>
- Adds all of them to an SQLite database <br>
- Lets you make SQL queries about the data <br>

### How to run:
```python3 fantasy.py fantasy.csv```

### Common SQL queries: 
```SELECT * FROM fantasy_scores;``` <br>
```SELECT * FROM fantasy_scores ORDER BY Passing_yards;```
