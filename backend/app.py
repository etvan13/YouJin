from flask import Flask, render_template, request, jsonify
import os

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define the paths to the templates and static folders
template_dir = os.path.join(project_root, 'frontend', 'templates')
static_dir = os.path.join(project_root, 'frontend', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

@app.route('/')
def index():
    return render_template('chatbot.html')

@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get('message')

    # TODO: Implement your AI processing here
    bot_response = process_message(user_message)

    return jsonify({'response': bot_response})

def process_message(message):
    # Placeholder for AI logic
    # For now, let's reverse the user's message as a simple example
    return message[::-1]

if __name__ == '__main__':
    app.run(debug=True)
