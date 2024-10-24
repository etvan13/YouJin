# ai_utils.py

import subprocess
import re
import threading
import fcntl
import os
import sys

def make_non_blocking(fd):
    # Make a file descriptor non-blocking
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

def process_output(output):
    """Cleans and processes terminal output by removing unwanted characters."""
    ansi_escape = re.compile(r'\x1b\[.*?m|\x1b\[.*?[A-Za-z]')
    cleaned_output = ansi_escape.sub('', output).strip()
    return cleaned_output if cleaned_output else None

def ai_terminal_interaction_loop(terminal_process, ai_model):
    """Manages the interaction loop between the terminal and the AI."""
    output_buffer = ''
    output_lock = threading.Lock()
    prompt_detected = threading.Event()

    def read_output():
        """Read and process the terminal output in a separate thread."""
        nonlocal output_buffer
        while True:
            try:
                output_line = terminal_process.stdout.readline()
                if output_line == '' and terminal_process.poll() is not None:
                    print("Terminal process has ended.")
                    prompt_detected.set()  # Ensure the main thread doesn't wait forever
                    break  # Terminal process ended

                processed_line = process_output(output_line)
                if processed_line is not None:
                    with output_lock:
                        output_buffer += processed_line + '\n'

                    # Print the output to the console (optional)
                    # print(processed_line)

                    # Check if prompt is detected
                    if processed_line.endswith('>'):
                        prompt_detected.set()

            except Exception as e:
                continue

    # Make stdout and stderr non-blocking
    make_non_blocking(terminal_process.stdout)
    make_non_blocking(terminal_process.stderr)

    # Start the output reader thread
    output_thread = threading.Thread(target=read_output)
    output_thread.daemon = True
    output_thread.start()

    while True:
        # Wait until prompt is detected
        prompt_detected.wait()
        prompt_detected.clear()

        # Get the packaged output
        with output_lock:
            packaged_output = output_buffer.strip()
            output_buffer = ''

        if not packaged_output:
            print("No packaged output, ending loop.")
            break  # Terminal process ended

        # Send to AI and get response
        ai_response = ai_model.process_input(packaged_output)
        if ai_response.lower() == 'exit':
            print("AI requested exit, ending loop.")
            break

        # Send AI response to terminal
        try:
            terminal_process.stdin.write(ai_response + '\n')
            terminal_process.stdin.flush()
        except BrokenPipeError as e:
            print(f"BrokenPipeError: {e}")
            break

    # Clean up terminal process
    terminal_process.terminate()
    terminal_process.wait()
    print("Terminal process terminated.")
