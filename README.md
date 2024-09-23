# YouJin(^-^)

YouJin utilizes **Llama** as the backend AI model integrated with a frontend chat interface. The coordinate system serves as a mechanism for the AI to navigate and access data stored through a custom terminal interface. Additional features will be implemented in future updates to expand the terminal's functionality, allowing for more dynamic interaction with the AI.

## Project Structure
- **Frontend**: A chat interface for interacting with the AI.
- **Backend**: Powered by Llama, handling AI processing and responses.
- **Terminal**: Uses a coordinate system to manage data storage and AI navigation.

## Getting Started

To set up and run the project on your local machine, follow the instructions below.

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/etvan13/YouJin.git
cd YouJin
```

### 2. Set Up the Virtual Environment

To ensure all dependencies are installed in an isolated environment, set up a Python virtual environment:

#### a. Create the Virtual Environment:

- On **Windows**:

    ```bash
    python -m venv venv
    ```

- On **macOS/Linux**:

    ```bash
    python3 -m venv venv
    ```

#### b. Activate the Virtual Environment:

- On **Windows**:

    ```bash
    venv\Scripts\activate
    ```

- On **macOS/Linux**:

    ```bash
    source venv/bin/activate
    ```

### 3. Install Dependencies

Once the virtual environment is activated, install the project dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Running the Project

The project runs in two parts: the frontend (user interface) and the backend (API server). Follow the instructions below to run both.

#### a. Start the Backend (Flask API):

1. Navigate to the `backend/` directory:
    ```bash
    cd backend
    ```

2. Run the Flask server:
    ```bash
    python app.py
    ```

This will start the backend server on http://localhost:5000. It will handle the AI logic and process the messages sent from the frontend.


#### b. Start the Frontend (HTML/CSS/JavaScript)

In a new terminal, do the following:

1. Navigate to the frontend/ directory:

    ```bash
    cd frontend
    ```

2. Start the frontend server using Python's built-in HTTP server:

    ```bash
    python -m http.server 8000
    ```

This will serve the frontend on http://localhost:8000.


### 5. Access the Chat Interface

Once both servers are running, open your web browser and navigate to:

```bash
http://localhost:8000/
```

From here, you can interact with the chatbot via the user interface.

* When you send a message from the frontend, it will be sent to the backend (running on http://localhost:5000).
* The backend processes the message and responds, and the frontend updates the chat interface with the response.

### 6. Deactivate the Virtual Environment (When Done)

When you're done working on the project, deactivate the virtual environment:
```bash
deactivate
```

## Future Development

* Backend Expansion: Future updates will include integration with the Llama AI for more advanced natural language processing and data retrieval.
* Terminal Interface: The terminal will be enhanced with additional commands, enabling more efficient data navigation through the coordinate system.
