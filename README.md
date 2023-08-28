# SurfsUP

This exercie contains a climate analysis for locations in Hawaii using 2 different methodologies.
The data provided can be found in the Resources folder.

The SurfsUp folder is divided into 2 sections:
1.) Climate Data using Python and SQLAlchemy --> HI_climate.ipynb
2.) Cliamte App using Flask API --> app.py

# The flask application has 5 routes:
1.) precipitation route: 
-precipitation and dates for the past year
2.) station route: 
-all stations in the database (full data provided)
3.) TOBS route: 
-data for the most active station for the past year (USC00519281)
4.) Date: 
-accepts a start date (YYYY-MM-DD) and returns MIN, MAX, and AVG temperature from the given start date
5.) DateRange: 
-accepts a start AND end date and returns MIN, MAX, and AVG temperature for the selected period