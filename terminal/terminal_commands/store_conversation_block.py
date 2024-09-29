# store_conversation_block.py

import json
import os

class StoreConversationBlockCommand:
    def __init__(self, terminal, conversation_block, increment_value=1):
        self.terminal = terminal
        self.conversation_block = conversation_block
        self.increment_value = increment_value

        # Get directory and define file paths
        command_dir = os.path.dirname(os.path.abspath(__file__))
        terminal_dir = os.path.dirname(command_dir)
        self.data_directory = os.path.join(terminal_dir, 'data')
        self.json_file = os.path.join(self.data_directory, 'conversation_blocks.json')

    def run(self):
        # Ensure the data directory exists
        os.makedirs(self.data_directory, exist_ok=True)

        # Get current coordinate and img_universe
        current_coordinate = self.terminal.coordinate.get_coordinates()
        current_img_universe = self.terminal.coordinate.get_img_univ()

        # Load existing conversation data, handling empty or malformed JSON
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r') as file:
                    content = file.read().strip()
                    if content:  # Only attempt to load JSON if content is non-empty
                        conversation_data = json.loads(content)
                    else:
                        conversation_data = {}
            except json.JSONDecodeError:
                print("Warning: JSON file is corrupted or not properly formatted. Initializing new data structure.")
                conversation_data = {}
        else:
            conversation_data = {}

        # Ensure the data for the current coordinate is a list
        if current_coordinate not in conversation_data:
            conversation_data[current_coordinate] = []  # Initialize with an empty list for blocks

        # Get existing universes at the current coordinate
        existing_universes = [
            block['universe'] for block in conversation_data[current_coordinate]
            if isinstance(block, dict) and 'universe' in block
        ]

        # Use the universe strategy to handle overlap, operating on the img_universe
        universe = self.terminal.universe_strategy.handle_overlap(existing_universes)

        # Add the new conversation block with the determined universe
        conversation_data[current_coordinate].append({
            "block": self.conversation_block,
            "universe": universe
        })

        # Save updated data back to the JSON file
        with open(self.json_file, 'w') as file:
            json.dump(conversation_data, file, indent=4)

        print(f"Stored conversation at coordinate {current_coordinate} in universe {universe}: {self.conversation_block}")

        # Set the terminal coordinate's img_universe to the new one
        self.terminal.coordinate.set_img_univ(universe)

        # Move to the next coordinate after storing
        for _ in range(self.increment_value):
            self.terminal.coordinate.increment()

        # Save the updated coordinate to the file (will only save the real universe)
        self.terminal.save_coordinate()

        # Output the new coordinate and img_universe
        print(f"Coordinate after increment: {self.terminal.coordinate.get_coordinates()} in img_universe {self.terminal.coordinate.get_img_univ()}")
