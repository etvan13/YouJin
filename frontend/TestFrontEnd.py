from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def chatbot_page():
    return render_template('index.html')

@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get('message')

    # For now, we'll just echo back the user's message with a placeholder response
    # In the future, you can integrate your AI model here
    bot_response = f"Echo: {user_message}"

    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
