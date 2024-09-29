# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get('message')

    # TODO: Add more complex AI logic here instead of simple input
    print(f"User: {user_message}")
    bot_response = input("Your response as AI: ")

    # Connect to the terminal (sending user message and bot response)

    return jsonify({'response': bot_response})



if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)
