# Baller Shot Caller

Baller Shot Caller is an interactive web-app where you try to predict shot outcomes using visualizations of NBA plays: http://www.ballershotcaller.net/. You play against the computer and try and guess who shot the ball. Each player is represented by a color; their runs start where the colors are lightest, and the play ends (i.e. a shot was taken) when the colors are darkest. Simply select who you think shot the ball, and click on "submit" to find out if you were correct. 



# nba-tracking
Georgetown Data Science NBA Player Tracking Project

Additional documentation 

/data contains raw files and data that can be referenced from the other python scripts' relative directory
Code from ingest with populate this folder with our json and csvs generated may be placed here.

/ingest contains our 
+ ingestion scripts that ingest from JSON to a MongoDB WORM store.
+ ingestion of the NBA play by play dataset from the API
+ export of data into tabular CSVs for storage

/dataReshape includes further munging steps, creating tables from our MongoDB worm store and also reshaping files from long to wide, and other similar munging tasks.

/exports contains visualizations and other data products

/ModelFitting contains a class in which to run several families of models


___

```
# To run environment setup script:
$ sh initenv.sh

# To activate virtualenv:
$ source .venv/bin/activate

# To deactivate:
$ deactivate
```
