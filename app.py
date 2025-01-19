import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()

uri=os.getenv("uri")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['weather_data_db']
collection = db["weather_collection"]
#print(collection)
try:
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
print(f"Database: {db.name}, Collection: {collection.name}")
print(f"Existing document count: {collection.count_documents({})}")

def load_weather_data_to_mongodb(path):
    try:
        df = pd.read_csv(path)

        #print(df.head())  
        #print(df.dtypes)
    
        required_columns = ['datetime_utc', ' _tempm', ' _hum', ' _pressurem']
        #print(df.columns)
        if not all(col in df.columns for col in required_columns):
            raise ValueError("CSV file must contain 'date', 'temp', 'humidity', and 'pressure' columns.")
        
        

        df = df[required_columns]

        
        df['datetime_utc'] = pd.to_datetime(df['datetime_utc'])

            
        # print(df.head())  
        # print(df.dtypes)  
        
        json_data = df.to_json(orient='records', date_format='iso')
        data = pd.read_json(json_data)
        result = collection.insert_many(data.to_dict('records'))
        print(f"Inserted {len(result.inserted_ids)} documents into MongoDB.")
        print("Weather data loaded into MongoDB successfully.")

    except Exception as e:
        print(f"Error loading data into MongoDB: {e}")


if collection.count_documents({}) == 0:
    load_weather_data_to_mongodb(path="testset.csv")

@app.route("/", methods=['GET', 'POST'])
def weather_page():
    if request.method == 'POST':
        city = "Delhi" 
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        return redirect(url_for('get_weather', city=city, start_date=start_date, end_date=end_date))
    return render_template('index.html')

@app.route("/get_weather", methods=['GET']) 
def get_weather():
    city = request.args.get('city')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    print(start_date, end_date)

    if not city or not start_date or not end_date:
        return jsonify({"error": "City, start_date, and end_date are required."}), 400

    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%dT00:00:00.000")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%dT23:59:59.999")
        query = {
            'datetime_utc': {'$gte': start_date_obj, '$lte': end_date_obj}
        }
        data = list(collection.find(query))

        if not data:
            return jsonify({'message': 'No data found for the specified date range'}), 404

        return render_template('get_weather.html', city=city, start_date=start_date, end_date=end_date, weather_data=data)
    except Exception as e:
        return jsonify({"error": f"Error fetching weather data: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port = 5001, debug=True)