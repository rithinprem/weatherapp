from flask import Flask, render_template, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

# Variable to indicate whether the application is active
app_active = True

# Function to reset the app_active variable after a certain time of inactivity
def reset_activity():
    global app_active
    while True:
        time.sleep(840)  # 14 minutes
        app_active = False

# Function to automatically ping the /ping endpoint at regular intervals
def automatic_ping():
    while True:
        # Ping the /ping endpoint within the application
        with app.test_request_context('/ping'):
            app.process_request(request.Request('/ping', method='GET'))

        time.sleep(600)  # Adjust the interval based on your needs (e.g., every 10 minutes)

# Start the background thread to reset activity
activity_reset_thread = threading.Thread(target=reset_activity)
activity_reset_thread.start()

# Start the background thread for automatic pinging
ping_thread = threading.Thread(target=automatic_ping)
ping_thread.start()

# Route for pinging to keep the application active
@app.route('/ping')
def ping():
    global app_active
    app_active = True
    return jsonify(status='ok')

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

# Before each request, check if the app should be considered active
@app.before_request
def before_request():
    global app_active
    if not app_active:
        # Perform any necessary actions to "wake up" the application
        # For example, you might make a request to another endpoint or perform initialization
        # In this example, we'll just set app_active to True
        app_active = True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

git commit -m "with threading"