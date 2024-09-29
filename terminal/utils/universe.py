# universe.py

from abc import ABC, abstractmethod

class UniverseTraversalStrategy(ABC):
    def __init__(self, terminal):
        self.terminal = terminal

    @abstractmethod
    def handle_overlap(self, existing_universes):
        """Determine the universe to use when an overlap occurs at a coordinate."""
        pass

    @staticmethod
    def select_universe_strategy(terminal, input_value=None):
        """
        Select universe traversal strategy either interactively or programmatically.
        If input_value is provided, use it; otherwise, prompt the user interactively.
        """
        strategy_map = {
            '1': LocalUniverseStrategy,
            '2': PersistentUniverseStrategy,
            '3': DynamicUniverseStrategy,
            'local': LocalUniverseStrategy,
            'persistent': PersistentUniverseStrategy,
            'dynamic': DynamicUniverseStrategy
        }

        # Use input_value if provided, otherwise prompt the user
        if input_value is None:
            print("Select universe traversal strategy:")
            print("1. Local Universe Strategy")
            print("2. Persistent Universe Strategy")
            print("3. Dynamic Universe Strategy")
            input_value = input("Enter the number or name of your choice: ")

        # Get strategy class based on input_value
        strategy_class = strategy_map.get(input_value.lower())
        if strategy_class:
            terminal.universe_strategy = strategy_class(terminal)
            return f"Universe traversal strategy set to {strategy_class.__name__}."
        else:
            return "Invalid choice. Strategy not changed."

### Local Universe Strategy ###
class LocalUniverseStrategy(UniverseTraversalStrategy):
    def handle_overlap(self, existing_universes):
        """
        Always use the lowest available universe at the coordinate,
        starting from the real universe value.
        """
        real_universe = self.terminal.coordinate.get_univ()

        # Generate possible universes starting from the real universe
        if existing_universes:
            max_existing_universe = max(existing_universes)
        else:
            max_existing_universe = real_universe - 1

        possible_universes = set(range(real_universe, max_existing_universe + 2))
        available_universes = possible_universes - set(existing_universes)

        if available_universes:
            universe = min(available_universes)
        else:
            universe = max_existing_universe + 1  # Increment beyond existing universes

        # Set the img_universe to the selected universe
        self.terminal.coordinate.set_img_univ(universe)
        return universe

### Persistent Universe Strategy ###
class PersistentUniverseStrategy(UniverseTraversalStrategy):
    def __init__(self, terminal):
        super().__init__(terminal)
        # Initialize universe to the img_universe value from the coordinate
        self.universe = terminal.coordinate.get_img_univ()

    def handle_overlap(self, existing_universes):
        """
        Maintain the img_universe across coordinates, incrementing it upon collision.
        """
        real_universe = self.terminal.coordinate.get_univ()
        # Ensure the universe is at least the real universe
        self.universe = max(self.universe, real_universe)

        if self.universe in existing_universes:
            self.universe = max(existing_universes) + 1

        # Set the img_universe to the selected universe
        self.terminal.coordinate.set_img_univ(self.universe)
        return self.universe

### Dynamic Universe Strategy ###
class DynamicUniverseStrategy(UniverseTraversalStrategy):
    """
    Dynamic Universe Strategy:
    - Try to move down by one universe if it's available (not below the real universe).
    - If no lower universe is available, stay in the current img_universe.
    - If the current img_universe is occupied, increment the img_universe by one.
    """
    def __init__(self, terminal):
        super().__init__(terminal)
        # No need to initialize self.universe; we'll use the coordinate's img_universe

    def handle_overlap(self, existing_universes):
        # Get the current img_universe and real universe from the coordinate
        current_img_universe = self.terminal.coordinate.get_img_univ()
        real_universe = self.terminal.coordinate.get_univ()

        # Case 1: Try to move down by one universe (not below real universe)
        lower_universe = current_img_universe - 1
        if lower_universe >= real_universe and lower_universe not in existing_universes:
            universe = lower_universe

        # Case 2: If the current img_universe is not occupied, use it
        elif current_img_universe not in existing_universes:
            universe = current_img_universe

        # Case 3: Current img_universe is occupied, lower universe is unavailable
        # Increment to the next available higher img_universe
        else:
            higher_universe = current_img_universe + 1
            while higher_universe in existing_universes:
                higher_universe += 1
            universe = higher_universe

        # Set the img_universe to the selected universe
        self.terminal.coordinate.set_img_univ(universe)
        return universe
