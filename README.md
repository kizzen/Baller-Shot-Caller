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

/VisualGame contains the python notebook needed to run 'ShotColla', the predictive game. 