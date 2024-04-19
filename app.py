from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
print("TOKEN_ENDPOINT:", os.getenv('TOKEN_ENDPOINT'))
print("DATA_ENDPOINT:", os.getenv('DATA_ENDPOINT'))
print("CLIENT_ID:", os.getenv('CLIENT_ID'))
print("USERNAME:", os.getenv('USER'))
print("PASSWORD:", os.getenv('PASSWORD'))
app = Flask(__name__)

# Retrieve the values from environment variables
TOKEN_ENDPOINT = os.getenv('TOKEN_ENDPOINT')
DATA_ENDPOINT = os.getenv('DATA_ENDPOINT')
CLIENT_ID = os.getenv('CLIENT_ID')
USERNAME = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/data/<string:event_code>/<string:participant_id>', methods=['GET'])
def data(event_code, participant_id):
    # Get the access token
    token_response = requests.post(
        TOKEN_ENDPOINT,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data={
            'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD,
            'client_id': CLIENT_ID
        }
    )
    token = token_response.json().get('access_token')

    print(token)


    # Use the token to get the data
    data_response = requests.get(
        f"{DATA_ENDPOINT}?eventCode={event_code}&filter={{\"participantIdOrUuid\": \"{participant_id}\"}}",
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
    )
    data = data_response.json()
    print("API Response:", data)
    # Render the data in the HTML table
    return render_template('table.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)