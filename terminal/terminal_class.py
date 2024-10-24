import json
import sys
import os

if __name__ == "__main__":
    # Add the parent directory to sys.path to locate utils when running as a script
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from terminal.utils.coordinate import Coordinate, FractionalCoordinate
    from terminal.utils.universe import UniverseTraversalStrategy
    from terminal.utils.universe import (
        LocalUniverseStrategy,
        PersistentUniverseStrategy,
        DynamicUniverseStrategy
    )
    from terminal.terminal_commands.store_conversation_block import StoreConversationBlockCommand

else:
    # Use relative imports when running as part of a package
    from .utils.coordinate import Coordinate, FractionalCoordinate
    from .utils.universe import UniverseTraversalStrategy
    from .utils.universe import (
        LocalUniverseStrategy,
        PersistentUniverseStrategy,
        DynamicUniverseStrategy
    )
    from .terminal_commands.store_conversation_block import StoreConversationBlockCommand




# Add new command imports here

class Terminal:
    def __init__(self, universe_strategy='local'):
        # Initialize coordinate and load saved state
        self.coordinate = Coordinate()
        
        terminal_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_directory = os.path.join(terminal_dir, 'data')
        self.coordinate_file = os.path.join(self.data_directory, 'current_coordinate.json')
        
        self.load_saved_coordinate()
        self.coordinate.reset_img_univ()
        self.set_universe_strategy(universe_strategy)  # Set initial universe strategy


        # Command dictionary for text-based input
        self.commands = {
            "help": self.show_help,
            "greetings": self.greet,
            "forwards": self.forwards_interactive,
            "backwards": self.backwards_interactive,
            "store_block": self.store_conversation_block_interactive,
            "universe_type": self.set_universe_strategy_interactive,
            # Add new commands here
        }

    #### DYNAMIC FUNCTIONS (*** FOR USE WITH BACKEND ***) ####

    def update_coordinate(self, delta): 
        """
        Let's you adjust the coordinate by delta amount 
        """
        # Call the interactive command
        if delta > 0:
            return self.forwards_interactive(delta)
        else:
            return self.backwards_interactive(abs(delta))

    def store_conversation_block(self, conversation_block, increment_value=1):
        """
        Stores the conversation block upon a certain coordinate.
        Default increments the coordinate by 1, but you can increment it however.
        """
        return self.store_conversation_block_interactive(conversation_block, increment_value)
        
    def set_universe_strategy(self, input_value):
        """
        Set the universe traversal strategy programmatically.
        Accepts either a number or a strategy name.
        """
        return self.set_universe_strategy_interactive(input_value)


    #### UTILITY FUNCTIONS ####

    @staticmethod
    def newpage():
        os.system('cls' if os.name == 'nt' else 'clear')

    def default_message(self):
        self.newpage()
        return f"{self.coordinate.get_coordinates()}\nType 'help' for a list of commands.\n"

    def process_command(self, command):
        if command in self.commands:
            response = self.commands[command]()
        else:
            response = "Unknown command."
        return f"{self.default_message()}\n{response}\n"

    def save_coordinate(self):
        os.makedirs(self.data_directory, exist_ok=True)
        coordinate_data = {
            "coordinate": self.coordinate.get_coordinates(),
            "coordinate_list": self.coordinate.get_coordinates_list(),
            "universe": self.coordinate.get_univ(),
        }
        with open(self.coordinate_file, 'w') as file:
            json.dump(coordinate_data, file, indent=4)

    def load_saved_coordinate(self):
        if os.path.exists(self.coordinate_file):
            with open(self.coordinate_file, 'r') as file:
                content = file.read().strip()
                if content:  # Only try to load JSON if the file is not empty
                    coordinate_data = json.loads(content)
                    self.coordinate.coordinates = coordinate_data.get("coordinate_list", [0, 0, 0, 0, 0])
                    self.coordinate.universes = coordinate_data.get("universes", 0)
                else:
                    print("JSON file is empty. Starting from default coordinate.")
        else:
            print("No saved coordinate found. Starting from [0, 0, 0, 0, 0].")


    #### TEXT-BASED INPUT COMMANDS (INTERACTIVE) ####

    def run(self):
        print(self.default_message())
        while True:
            command = input("> ").lower()
            if command == "exit":
                break
            output = self.process_command(command)
            print(output)

    def show_help(self):
        command_list = sorted(self.commands.keys())
        help_text = "\n".join(f"- {cmd}" for cmd in command_list)
        return help_text

    def greet(self):
        return "Hello Universe!"

    def forwards_interactive(self, delta=1):
        """
        Interactive logic for moving the coordinate forward.
        """
        self.coordinate.spec_change(delta)
        self.save_coordinate()
        return f"Moved forwards by {delta}."

    def backwards_interactive(self, delta=1):
        """
        Interactive logic for moving the coordinate backward.
        """
        self.coordinate.spec_change(-delta)
        self.save_coordinate()
        return f"Moved backwards by {delta}."

    def store_conversation_block_interactive(self, conversation_block=None, increment_value=1):
        """
        Interactive logic for storing a conversation block.
        Prompts for input if no conversation block is provided.
        """
        if conversation_block is None:
            user_message = input("Input user part of block: ")
            ai_response = input("Input AI part of block: ")
            conversation_block = {"user": user_message, "bot": ai_response}
        
        # Initialize and run the command to store the conversation block
        command = StoreConversationBlockCommand(self, conversation_block, increment_value)
        command.run()
        return f"Conversation block stored. Coordinate incremented by {increment_value}."
    
    def set_universe_strategy_interactive(self, input_value=None):
        """
        Interactive command to select the universe traversal strategy.
        If input_value is provided, use it; otherwise, prompt the user interactively.
        """
        return UniverseTraversalStrategy.select_universe_strategy(self, input_value)




    #### ADDITIONAL COMMANDS ####

    # Add any new text-based input commands below this line
    # For example:
    # def another_command(self):
    #     return "This is another command."



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