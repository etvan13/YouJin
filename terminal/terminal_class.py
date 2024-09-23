import os
from utils.coordinate import Coordinate, FractionalCoordinate

# Import command classes

# Add new command imports here

class Terminal:
    def __init__(self):
        self.coordinate = Coordinate()  # Initialize the coordinate object
        self.commands = {
            "help": self.show_help,
            "greetings": self.greet,
            "forwards": self.forwards,
            "backwards": self.backwards,
            # Add new commands here
        }

    # Clear the console screen
    @staticmethod
    def newpage():
        os.system('cls' if os.name == 'nt' else 'clear')

    # Header message of terminal
    def default_message(self):
        self.newpage()
        return f"{self.coordinate.get_coordinates()}\n" + "Type 'help' for a list of commands.\n"
    
    # Checks the inputted command for validity returning its output
    def process_command(self, command):
        if command in self.commands:
            response = self.commands[command]()
        else:
            response = "Unknown command."
        return self.default_message() + "\n" + response + "\n"  # Append a newline

    # Runs the current Terminal
    def run(self):
        # Start the terminal with the default message
        print(self.default_message())  
        while True:
            command = input("> ").lower()
            output = self.process_command(command)
            print(output)
            if command == "exit":
                break
    
    # Filler for adding external commands
    def add_external_command(self, command_name, command_function):
        self.commands[command_name] = command_function

    ####COMMANDS####
    
    # Dynamically prints a list of available commands
    def show_help(self):
        command_list = sorted(self.commands.keys())  # Sort for readability
        help_text = "\n".join(f"- {cmd}" for cmd in command_list)
        return help_text
    
    # Returns a greeting
    def greet(self):
        return "Hello Universe!"

    # Moves the coordinate object forwards 1
    def forwards(self):
        self.coordinate.increment()
        return "Moved forwards."

    # Moves the coordinate object backwards 1
    def backwards(self):
        self.coordinate.decrement()
        return "Moved backwards."
    

    ####### Add additional Commands Above here ########


### EXAMPLE COMMANDS ###

class ExampleSimpleCommand:
    """
    This is a simple command example.
    """

    def __init__(self):
        pass  # Initialize any required variables here

    def run(self):
        print("This is an example of a simple command.")


class ExampleCommandWithSubcommands:
    """
    This is an example of a command with sub-commands.
    """

    def __init__(self):
        self.commands = {
            "help": self.show_help,
            "subcommand1": self.subcommand1,
            "subcommand2": self.subcommand2,
            # Add more sub-commands here
        }

    def show_help(self):
        help_message = "Available sub-commands:\n"
        for cmd in self.commands:
            help_message += f"- {cmd}\n"
        print(help_message.strip())

    def subcommand1(self):
        print("Executed subcommand1.")

    def subcommand2(self):
        print("Executed subcommand2.")

    def run(self):
        print("Entering example command with sub-commands. Type 'help' for options.")
        while True:
            command_input = input("ExampleCommand> ").lower()
            if command_input == "exit":
                print("Exiting example command.")
                break
            elif command_input in self.commands:
                self.commands[command_input]()
            else:
                print("Unknown sub-command. Type 'help' for options.")


# For running and testing the terminal

def main():
    terminal = Terminal()
    terminal.run()


if __name__ == "__main__":
    main()