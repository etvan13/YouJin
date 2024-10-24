import os
import sys

# Get the current directory of app.py (i.e., backend directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add the project root directory to sys.path to access terminal_class
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(PROJECT_ROOT)

from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_type import AI_Type  # Import the AI_Type class
from terminal.terminal_class import Terminal

app = Flask(__name__)
CORS(app)

# Initialize the Terminal object for storing conversation blocks
terminal = Terminal()

# Initialize the AI system
ai_system = AI_Type()

# Store the selected AI method in an environment variable
def select_ai_method():
    """Prompt the user in the terminal to select an AI method, including 'user_input'."""
    if os.getenv("SELECTED_AI_METHOD"):
        print(f"AI method already selected: {os.getenv('SELECTED_AI_METHOD')}")
        return  # Don't ask again if the method is already selected

    available_ais = ai_system.get_available_ais()

    # Include 'user_input' as an option, so it can be explicitly selected
    print("Available AI methods:")
    for idx, ai_name in enumerate(available_ais, start=1):
        print(f"{idx}. {ai_name}")

    while True:
        try:
            choice = int(input("Select an AI method by entering the corresponding number: "))
            if 1 <= choice <= len(available_ais):
                selected_ai_method = available_ais[choice - 1]
                os.environ["SELECTED_AI_METHOD"] = selected_ai_method  # Store the selection in an environment variable
                print(f"Selected AI method: {selected_ai_method}")
                return
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Route to process user input
@app.route('/get-response', methods=['POST'])
def get_response():
    """Process user input using the selected AI method."""
    selected_ai_method = os.getenv("SELECTED_AI_METHOD")
    
    if not selected_ai_method:
        return jsonify({'error': 'No AI method selected. Please select an AI method first.'}), 400

    data = request.get_json()
    user_message = data.get('message')

    # Run the selected AI and get the response
    bot_response = ai_system.run_selected_ai(selected_ai_method, user_message)

    # Store the conversation block using the Terminal object
    conversation_block = {"user": user_message, "bot": bot_response}
    terminal.store_conversation_block(conversation_block)

    # Return the response as JSON
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    # Prompt the user to select an AI method when the app starts
    select_ai_method()
    app.run(port=5000, debug=True, threaded=True)
