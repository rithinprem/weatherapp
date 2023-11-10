from flask import Flask, render_template, request, jsonify
import requests
import schedule
import time
import threading

app = Flask(__name__)


@app.route("/ping")
def ping():
    print("pinging..")
    return jsonify(status="ok")


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



def send_request():
    # Define the URL you want to send the request to
    url = 'http://localhost:5003/ping'

    # Make the HTTP request using the 'requests' library
    response = requests.get(url)

    # Access the response content
    content = response.content

    # Process the content or log it as needed
    print(content)

def run_flask():
    app.run(host="0.0.0.0", port=5003, threaded=True)

if __name__ == "__main__":
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Schedule the job to run every 10 minutes
    schedule.every(10).minutes.do(send_request)

    # Run the scheduled jobs continuously
    while True:
        schedule.run_pending()
        time.sleep(1)
