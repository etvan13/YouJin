import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from terminal.terminal_class import Terminal

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create a terminal instance
terminal = Terminal()

@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get('message')

    # TODO: Add more complex AI logic here instead of simple input
    print(f"User: {user_message}")
    bot_response = input("Your response as AI: ")

    # Create a conversation block and send it to the terminal
    conversation_block = {"user": user_message, "bot": bot_response}

    # Use the terminal instance to store the conversation block
    terminal.store_conversation_block(conversation_block)

    return jsonify({'response': bot_response})


if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)
