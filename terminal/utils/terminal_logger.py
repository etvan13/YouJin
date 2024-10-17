import os
import platform
import subprocess
import datetime
import re
import sys
import threading
import fcntl

# Define the directory to store log files
LOG_DIR = os.path.join(os.path.dirname(__file__), 'terminal_log_data')
os.makedirs(LOG_DIR, exist_ok=True)  # Create the directory if it doesn't exist

# Get the current date and time for the log file
now = datetime.datetime.now()
log_filename = f"terminal_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
log_filepath = os.path.join(LOG_DIR, log_filename)

# Function to make file descriptors non-blocking (required for non-blocking read)
def make_non_blocking(fd):
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

def log_terminal():
    """Function to log terminal output with formatted input/output blocks."""
    try:
        # Start the terminal_class.py script with unbuffered I/O
        terminal_script_path = os.path.join(os.path.dirname(__file__), '..', 'terminal_class.py')
        terminal_process = subprocess.Popen(
            ['python3', terminal_script_path],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=1
        )

        print(f"Terminal session started and logging to {log_filepath}")

        # Make stdout and stderr non-blocking
        make_non_blocking(terminal_process.stdout)
        make_non_blocking(terminal_process.stderr)

        # Open the log file for writing
        with open(log_filepath, 'w') as log_file:
            # Function to clean and process output lines
            def process_output(output):
                # Remove escape sequences (e.g., screen clears)
                ansi_escape = re.compile(r'\x1b\[.*?m|\x1b\[.*?[A-Za-z]')
                cleaned_output = ansi_escape.sub('', output).strip()

                # Filter out unwanted outputs
                unwanted_outputs = ['Coordinate saved', 'Coordinate loaded']
                for unwanted in unwanted_outputs:
                    if unwanted in cleaned_output:
                        return None  # Skip this line

                # Ignore empty lines
                if cleaned_output == '':
                    return None

                return cleaned_output

            def read_output():
                """Read and process the terminal output in a separate thread."""
                output_block = ''
                while True:
                    try:
                        output_line = terminal_process.stdout.readline()
                        if output_line == '' and terminal_process.poll() is not None:
                            break  # Terminal process ended

                        processed_line = process_output(output_line)
                        if processed_line is not None:
                            # Accumulate output block until the prompt (">") is detected
                            output_block += processed_line + '\n'

                            if processed_line.endswith('>'):
                                # Log the entire output block once prompt is detected
                                log_file.write('output:\n')
                                log_file.write(output_block)
                                log_file.write('\n')
                                log_file.flush()  # Ensure real-time logging

                                # Print the output block to the screen
                                print(output_block, end='')

                                # Clear the accumulated output block
                                output_block = ''

                    except Exception as e:
                        continue

            # Run the output reader in a separate thread
            output_thread = threading.Thread(target=read_output)
            output_thread.daemon = True
            output_thread.start()

            # Main interaction loop for user input
            while True:
                # Get user input
                user_input = input('')

                if user_input.strip().lower() == 'exit':
                    break

                log_file.write('input:\n')
                log_file.write(user_input + '\n\n')
                log_file.flush()

                # Send input to terminal process
                terminal_process.stdin.write(user_input + '\n')
                terminal_process.stdin.flush()

            # Terminate the terminal process if it is still running
            terminal_process.terminate()
            terminal_process.wait()

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def main():
    """Main function to start logging."""
    log_terminal()

if __name__ == "__main__":
    main()
