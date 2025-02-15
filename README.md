# Securin_Assessment_Anirudh

# Weather Data Analysis Application

## Description
This is a Flask-based web application that provides weather data analysis capabilities. The application allows users to view and analyze weather data stored in MongoDB, including temperature, humidity, and pressure measurements. Users can filter data by date ranges and perform yearly temperature analysis.

## Features
- View weather data for specified date ranges
- Analyze yearly temperature trends with monthly breakdowns
- Interactive web interface
- MongoDB integration for data storage
- Support for CSV data import

## Prerequisites
- Python 3.x
- MongoDB
- Required Python packages:
  - Flask
  - pymongo
  - pandas
  - python-dotenv

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install required packages:
```bash
pip install flask pymongo pandas python-dotenv
```

3. Create a `.env` file in the project root and add your MongoDB connection string:
```
uri=your_mongodb_connection_string
```

## Data Setup
The application expects a CSV file named `testset.csv` with the following columns:
- datetime_utc
- _tempm (temperature)
- _hum (humidity)
- _pressurem (pressure)

The data will be automatically loaded into MongoDB if the collection is empty.

## Usage

1. Start the application:
```bash
python app.py
```

2. Access the application at `http://localhost:5001`

3. Available Routes:
- `/`: Home page with date range selection
- `/get_weather`: Displays weather data for selected date range
- `/yearly-analysis`: Provides yearly temperature analysis with monthly breakdowns

## API Endpoints

### GET /get_weather
Returns weather data for a specified date range.

Query Parameters:
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `city`: City name

### POST /yearly-analysis
Provides yearly temperature analysis.

Form Parameters:
- `year`: Year for analysis (YYYY)

## Error Handling
- The application includes comprehensive error handling for:
  - Database connection issues
  - Invalid date ranges
  - Missing data
  - Invalid input parameters

## Technical Details
- The application runs on port 5001 by default
- MongoDB is used as the primary database
- Data filtering is implemented using MongoDB queries
- Temperature analysis includes high, low, and median calculations

## Development
The application runs in debug mode by default. To disable debug mode for production, modify the last line in `app.py`:

```python
app.run(port=5001, debug=False)
```







