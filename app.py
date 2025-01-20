import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from statistics import median

app = Flask(__name__)

load_dotenv()

uri = os.getenv("uri")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['weather_data_db']
collection = db["weather_collection"]

try:
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

def load_weather_data_to_mongodb(path):
    try:
        df = pd.read_csv(path)
        required_columns = ['datetime_utc', ' _tempm', ' _hum', ' _pressurem']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("CSV file must contain 'datetime_utc', ' _tempm', ' _hum', and ' _pressurem' columns.")

        df = df[required_columns]
        df['datetime_utc'] = pd.to_datetime(df['datetime_utc'])

        json_data = df.to_json(orient='records', date_format='iso')
        data = pd.read_json(json_data)
        collection.insert_many(data.to_dict('records'))
        print(f"Inserted {len(data)} documents into MongoDB.")

    except Exception as e:
        print(f"Error loading data into MongoDB: {e}")

if collection.count_documents({}) == 0:
    load_weather_data_to_mongodb(path="testset.csv")

def build_filter_query(start_date, end_date, temp_min=None, temp_max=None, 
                      humidity_min=None, humidity_max=None, 
                      pressure_min=None, pressure_max=None):
    query = {
        'datetime_utc': {
            '$gte': datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%dT00:00:00.000"),
            '$lte': datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%dT23:59:59.999")
        }
    }
    
    if temp_min is not None or temp_max is not None:
        query[' _tempm'] = {}
        if temp_min is not None:
            query[' _tempm']['$gte'] = float(temp_min)
        if temp_max is not None:
            query[' _tempm']['$lte'] = float(temp_max)

    if humidity_min is not None or humidity_max is not None:
        query[' _hum'] = {}
        if humidity_min is not None:
            query[' _hum']['$gte'] = float(humidity_min)
        if humidity_max is not None:
            query[' _hum']['$lte'] = float(humidity_max)

    if pressure_min is not None or pressure_max is not None:
        query[' _pressurem'] = {}
        if pressure_min is not None:
            query[' _pressurem']['$gte'] = float(pressure_min)
        if pressure_max is not None:
            query[' _pressurem']['$lte'] = float(pressure_max)

    return query

@app.route("/", methods=['GET', 'POST'])
def index_page():
    if request.method == 'POST':
        city = "Delhi"
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')


        return redirect(url_for('get_weather', city=city, start_date=start_date, end_date=end_date))
    return render_template('index.html')

@app.route("/get_weather", methods=['GET'])
def get_weather():
    try:
        params = request.args
        start_date_obj = datetime.strptime(params.get('start_date'), "%Y-%m-%d").strftime("%Y-%m-%dT00:00:00.000")
        end_date_obj = datetime.strptime(params.get('end_date'), "%Y-%m-%d").strftime("%Y-%m-%dT23:59:59.999")
        query = {
        'datetime_utc': {'$gte': start_date_obj, '$lte': end_date_obj}
        }
        data = list(collection.find(query))

        if not data:
            return jsonify({'message': 'No data found for the specified date range'}), 404
        return render_template('get_weather.html', city=params.get('city'), 
                            start_date=params.get('start_date'), 
                            end_date=params.get('end_date'), 
                            weather_data=data)
        
    except Exception as e:
        return jsonify({"error": f"Error fetching weather data: {str(e)}"}), 500


@app.route("/yearly-analysis", methods=['POST'])
def yearly_analysis():
    try:
        year = request.form.get('year')
        if not year:
            return jsonify({"error": "Year is required"}), 400

        start_date = f"{year}-01-01T00:00:00.000"
        end_date = f"{year}-12-31T23:59:59.999"

        query = {
            'datetime_utc': {
                '$gte': start_date,
                '$lte': end_date
            }
        }

        data = list(collection.find(query))

        if not data:
            return render_template('yearly_analysis.html', year=year, monthly_data={}, 
                                   error="No data found for the specified year")

        df = pd.DataFrame(data)
        df['datetime_utc'] = pd.to_datetime(df['datetime_utc'])
        df['month'] = df['datetime_utc'].dt.strftime('%B')

        monthly_data = {}
        for month in df['month'].unique():
            month_data = df[df['month'] == month][' _tempm']
            monthly_data[month] = {
                'high': float(month_data.max()),
                'low': float(month_data.min()),
                'median': float(month_data.median())
            }

        return render_template('yearly_analysis.html', 
                               year=year, 
                               monthly_data=monthly_data)

    except Exception as e:
        return jsonify({"error": f"Error analyzing temperature data: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
