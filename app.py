from flask import Flask, render_template, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/weatherapp', methods=['POST', 'GET'])
def get_weatherdata():
    url = "https://api.weatherapi.com/v1/current.json?"
    params = {"key": "2a0ca514d16545f3a0622421231011", "q": request.form.get("city")}
    response = requests.get(url, params)
    data = response.json()
    return render_template("output.html", weather_data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)