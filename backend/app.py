import sys
import os
import importlib.util
import inspect
from flask import Flask, request, jsonify, Response
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
            # Dynamically load run_model.py
            spec = importlib.util.spec_from_file_location("run_model", RUN_MODEL_PATH)
            run_model = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(run_model)

            # Check if 'process_input' accepts 'token_callback' parameter
            process_input_sig = inspect.signature(run_model.process_input)
            supports_streaming = 'token_callback' in process_input_sig.parameters

            if supports_streaming:
                # Function to yield tokens as a streaming response
                def token_stream():
                    final_response = ""

                    def token_callback(token):
                        nonlocal final_response
                        final_response += token
                        yield token

                    # Generate response using the process_input function with streaming
                    run_model.process_input(user_message, token_callback=token_callback)

                    # Store the final response block after streaming completes
                    conversation_block = {"user": user_message, "bot": final_response}
                    terminal.store_conversation_block(conversation_block)

                # Return the token stream as a Flask response
                return Response(token_stream(), content_type='text/plain')

            else:
                # If streaming is not supported, get the full response
                bot_response = run_model.process_input(user_message)

                # Store the conversation block
                conversation_block = {"user": user_message, "bot": bot_response}
                terminal.store_conversation_block(conversation_block)

                # Return the response as JSON
                return jsonify({'response': bot_response})

        except Exception as e:
            print(f"Error running AI model: {e}")
            return jsonify({"response": "Sorry, something went wrong with the AI."}), 500
    else:
        # Fallback to manual terminal input
        print(f"User: {user_message}")
        bot_response = input("Your response as AI: ")
        conversation_block = {"user": user_message, "bot": bot_response}
        terminal.store_conversation_block(conversation_block)
        return jsonify({'response': bot_response})

@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get('message')

    # Route the user message to AI model or fallback
    return run_model_or_fallback(user_message)

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)
