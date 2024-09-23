from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS if frontend is on a different port

@app.route('/generate-response', methods=['POST'])
def generate_response():
    data = request.get_json()
    user_message = data.get('message')

    # TODO: Replace with actual AI logic
    ai_response = process_user_message(user_message)

    return jsonify({'response': ai_response})

def process_user_message(message):
    # Placeholder for AI processing
    return f"AI Response: {message}"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
