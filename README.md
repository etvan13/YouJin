# Chatbot with Llama AI and Coordinate-Based Data Navigation

This project leverages **Llama** as the backend AI model integrated with a frontend chat interface. The coordinate system serves as a mechanism for the AI to navigate and access data stored through a custom terminal interface. Additional features will be implemented in future updates to expand the terminal's functionality, allowing for more dynamic interaction with the AI.

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

### 4. Running the Frontend

To start the frontend (currently using Flask), follow these steps:

#### a. Run the Flask Development Server:

Make sure you are in the `project-root/frontend/` directory, and run the following command to start the Flask server:

```bash
python TestFrontEnd.py
```

This will start the frontend on http://localhost:5000/. You can interact with the AI via the chat interface in your browser.

### 5. Deactivate the Virtual Environment (When Done)

When you're done working on the project, deactivate the virtual environment:
```bash
deactivate
```

# Future Development

* Backend Expansion: Future updates will include integration with the Llama AI for more advanced natural language processing and data retrieval.
* Terminal Interface: The terminal will be enhanced with additional commands, enabling more efficient data navigation through the coordinate system.