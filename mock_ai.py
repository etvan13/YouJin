# mock_ai.py

import subprocess
from terminal.utils import ai_utils  # Import the utility functions for handling terminal interaction

class MockAI:
    """A simulated AI that allows the user to input responses manually for testing purposes."""
    
    def process_input(self, packaged_output):
        """
        Shows the terminal output to the user and prompts for an input command.
        """
        print(packaged_output)  # Print the terminal output package for visibility
        # Prompt the user for the AI's response
        ai_response = input()
        return ai_response.strip()

    def test_terminal_interaction(self):
        """
        Runs a loop to test the interaction between the terminal and the AI,
        allowing you to manually input commands and simulate AI behavior.
        """
        # Start the terminal process (ensure the correct path to your terminal_class.py script)
        terminal_script_path = 'terminal/terminal_class.py'  # Adjust the path if necessary
        try:
            terminal_process = subprocess.Popen(
                ['python3', terminal_script_path],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=1
            )
            print("Terminal process started successfully.")
        except Exception as e:
            print(f"Error starting terminal process: {e}")
            return

        # Use the ai_utils file to manage the interaction loop
        ai_utils.ai_terminal_interaction_loop(terminal_process, self)

if __name__ == "__main__":
    mock_ai = MockAI()
    # Call the test function to manually input commands and simulate interaction
    mock_ai.test_terminal_interaction()
