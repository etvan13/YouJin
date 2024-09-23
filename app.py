# app.py

from flask import Flask, render_template, request, jsonify
from backend.response_generator import generate_response

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

@app.route('/')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get('message')

    bot_response = generate_response(user_message)

    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
