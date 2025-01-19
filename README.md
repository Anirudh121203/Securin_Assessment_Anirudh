# Securin_Assessment_Anirudh

# Weather Data Application

## Overview
This Flask application manages historical weather data, storing it in MongoDB and providing a web interface to query weather information for specific date ranges. The application loads weather data from a CSV file and allows users to retrieve weather information through a web interface.

## Features
- Load weather data from CSV files into MongoDB
- Web interface for querying weather data by date range
- Automatic data initialization from CSV if database is empty
- Error handling and data validation
- Real-time weather data retrieval and display

## Prerequisites
- Python 3.7+
- MongoDB Atlas account or local MongoDB installation
- CSV file with weather data containing required columns

## Required Python Packages
```bash
pip install flask
pip install pymongo
pip install pandas
pip install python-dotenv
```

## Project Structure
```
weather-app/
├── app.py
├── .env
├── testset.csv
├── templates/
│   ├── index.html
│   └── get_weather.html
└── README.md
```

## Setup Instructions

### 1. Environment Configuration
Create a `.env` file in the project root with your MongoDB connection string:
```
uri=your_mongodb_connection_string
```

### 2. Data Requirements
Ensure your CSV file (`testset.csv`) contains the following columns:
- `datetime_utc`: Timestamp in UTC
- `_tempm`: Temperature in Celsius
- `_hum`: Humidity percentage
- `_pressurem`: Atmospheric pressure

### 3. MongoDB Setup
The application will automatically:
- Connect to MongoDB using the provided URI
- Create a database named `weather_data_db`
- Create a collection named `weather_collection`
- Load data from CSV if the collection is empty

## Running the Application

1. Clone the repository
```bash
git clone <repository-url>
cd weather-app
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the Flask application
```bash
python app.py
```

The application will start on `http://localhost:5001`

## Usage

### Web Interface
1. Access the application at `http://localhost:5001`
2. Select start and end dates in the form
3. Submit to view weather data for the specified date range

### API Endpoints

#### 1. Home Page
- **URL:** `/`
- **Methods:** `GET`, `POST`
- **Description:** Displays the main input form

#### 2. Get Weather Data
- **URL:** `/get_weather`
- **Method:** `GET`
- **Query Parameters:**
  - `city` (string): City name (currently fixed to "Delhi")
  - `start_date` (string): Start date (YYYY-MM-DD)
  - `end_date` (string): End date (YYYY-MM-DD)









