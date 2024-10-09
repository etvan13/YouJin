import sys
import os
import importlib.util
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Get the current directory of app.py (i.e., backend directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add the project root directory to sys.path to access terminal_class
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(PROJECT_ROOT)

# Import Terminal class from the project root's terminal module
from terminal.terminal_class import Terminal
terminal = Terminal()

# Path to the AI model script (run_model.py) inside the backend/ai directory
RUN_MODEL_PATH = os.path.join(BASE_DIR, 'ai', 'run_model.py')

# Function to load and run the AI model if available
def run_model_or_fallback(user_message):
    if os.path.exists(RUN_MODEL_PATH):
        try:
            # Dynamically load and run run_model.py
            spec = importlib.util.spec_from_file_location("run_model", RUN_MODEL_PATH)
            run_model = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(run_model)
            
            # Pass user_message to run_model.py's process_input function
            if hasattr(run_model, 'process_input'):
                return run_model.process_input(user_message)
            else:
                raise AttributeError("run_model.py does not have a 'process_input' function.")
        except Exception as e:
            print(f"Error running AI model: {e}")
            return "Sorry, something went wrong with the AI."
    else:
        # Fallback to manual terminal input
        print(f"User: {user_message}")
        return input("Your response as AI: ")

@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get('message')

    # Route the user message to AI model or fallback
    bot_response = run_model_or_fallback(user_message)

    # Log the conversation and return the response
    conversation_block = {"user": user_message, "bot": bot_response}
    terminal.store_conversation_block(conversation_block)

    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)
