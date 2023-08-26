# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/TOBS USC00519281<br/>"
        f"/api/v1.0/date/<br/>"
        f"/api/v1.0/DateRange/<br/>"
    )

# Set variable to calculate and return the date one year from the most recent date. To be used to answer question 1
def date_prev_year():
    # Create the session
    session = Session(engine)

    # Define the most recent date in the Measurement dataset
    # Then use the most recent date to calculate the date one year from the last date
    most_recent_date = session.query(func.max(Measurement.date)).first()[0]
    first_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Close the session                   
    session.close()

    # Return the date
    return(first_date)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session
    session = Session(engine)

    # Query precipitation data from last 12 months from the most recent date from Measurement table. Use date_prev_year in filter
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date_prev_year()).all()
    
    # Close the session                   
    session.close()

    # Create a dictionary from the row data and append to a list of prcp_list
    prcp_list = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    # Return a list of jsonified precipitation data for the previous 12 months 
    return jsonify(prcp_list)

#Return a list of station data including the station_id, name, latitude, longitude, and elevation of each station

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)

#Query the dates and temperature observations of the most-active station for the previous year of data.
#Most activate station is USC00519281, which was found in previous analysis

@app.route("/api/v1.0/TOBS USC00519281")
def TOBS():
    # Create the session
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the previous year of data.
    USC00519281_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281')\
        .filter(Measurement.date >= date_prev_year()).all()

    # Close the session                   
    session.close()

    # Create a dictionary from the row data and append to a list for the most active station
    USC00519281_list = []
    for date, tobs in USC00519281_data:
        USC00519281_dict = {}
        USC00519281_dict["date"] = date
        USC00519281_dict["tobs"] = tobs
        USC00519281_list.append(USC00519281_dict)

    # Return a list of jsonified precipitation data for the previous 12 months 
    return jsonify(USC00519281_list)

#Specified start, calculates MIN, AVG, and MAX for all the dates greater than or equal to the start date.
#Start date is dynamic input entered by user.

@app.route("/api/v1.0/date/<configdate>")
def get_start(configdate):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Return MIN, MAX, and AVG Temperatures (tobs) for all stations after the given input date from user.
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date >= configdate).all()

    #session.close()

    stats = []
    for min, avg, max in results:
        stats_dict = {}
        stats_dict ["Min"] = min
        stats_dict ["Max"] = max
        stats_dict ["Avg"] = avg
        stats.append(stats_dict)

    return jsonify(stats)

#Specified start date and end date, calculate MIN, AVG, and MAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/DateRange/<start_date>/<end_date>")
def get_age(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data between an age range"""
    # Query all passengers by gender
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start_date)\
        .filter(Measurement.date <= end_date) \
        .all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    stats = []
    for min, avg, max in results:
        stats_dict = {}
        stats_dict ["Min"] = min
        stats_dict ["Max"] = max
        stats_dict ["Avg"] = avg
        stats.append(stats_dict)

    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)