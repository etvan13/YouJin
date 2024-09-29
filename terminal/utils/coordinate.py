class Coordinate:
    # Initialize object
    def __init__(self):
        self.coordinates = [0] * 5  # Initialize six coordinates
        self.universes = 0 # Initialize universes coordinate
        self.img_universe = 0  # Track the imaginary universe

    # Copy constructor
    def copy(self):
        # Create a new instance of Coordinate
        new_coordinate = Coordinate()
        # Copy the coordinates array
        new_coordinate.coordinates = self.coordinates[:]
        return new_coordinate

    # Increase coordinate by 1
    def increment(self):
        self._update_coordinates(1)

    # Decrease coordinate by 1
    def decrement(self):
        self._update_coordinates(-1)
    
    # Special increment based on value
    def spec_change(self, value):
        self._update_coordinates(value)

    # Takes inputted number and alters coordinates by that value
    def _update_coordinates(self, delta):
        # Start from the first coordinate and update
        for i in range(len(self.coordinates)):
            self.coordinates[i] += delta
            # Check for roll-over or roll-under
            if delta > 0 and self.coordinates[i] == 60:
                self.coordinates[i] = 0
                if i == len(self.coordinates) - 1:
                    self.universes += 1  # Increment universes if the last coordinate rolls over
                continue
            elif delta < 0 and self.coordinates[i] == -1:
                self.coordinates[i] = 59
                if i == len(self.coordinates) - 1:
                    self.universes -= 1  # Decrement universes if the last coordinate rolls under
                continue
            break  # Stop updating if no carry-over or borrow
    
    # Splits the coordinate string into a list of coordinates
    @staticmethod
    def parse_coordinate(coord_str):
        if ' ' in coord_str:
            # Split the string by spaces and validate each part
            parts = coord_str.split()
            if len(parts) != 6 or not all(part.isdigit() and int(part) < 60 for part in parts):
                raise ValueError("Invalid coordinate format. Each number must be less than 60. Expected format: # # # # # #")
            return [int(x) for x in parts]
        else:
            raise ValueError("Invalid input. Expected a coordinate input.")

    # Joins the coordinate list into a string format # # # # # #
    def get_coordinates(self):
        # Returns the coordinates in a formatted string
        return ' '.join(str(c) for c in self.coordinates)
    
    def get_coordinates_list(self):
        return self.coordinates

    # Converts list of coordinates (Each a subsequent power of 60) into a single base 10 number
    def baseTenConv(self, digits=None):
        """
        Convert the internal coordinates or an external list of base-60 digits to a base-10 number.
        
        :param digits: (Optional) List of integers representing the base-60 digits.
        :return: Base-10 integer.
        """
        if digits is None:
            digits = self.coordinates

        return sum(d * (60 ** i) for i, d in enumerate(digits))

    # Returns a string coordinate given a base 10 number
    def strCoord_conv(self, number):
        number %= (60 ** 5)  # Modulo to get the value within the current universe

        digits = []
        while number > 0:
            digits.append(number % 60)
            number //= 60

        while len(digits) < 5:
            digits.append(0)

        return ' '.join(str(d) for d in digits)
    
    # Returns a list coordinate for calculations given a number
    def coord_conv(self, number):
        number %= (60 ** 6)  # Modulo to get the value within the current universe

        digits = []
        while number > 0:
            digits.append(number % 60)
            number //= 60

        while len(digits) < 5:
            digits.append(0)

        return digits
    
    # Returns universe count (Amount of times overflow happens)
    def get_univ(self):
        return self.universes  # Return the number of universes
    
    def set_univ(self, delta):
        self.universes = delta

    # Returns imaginary universe count
    def get_img_univ(self):
        return self.img_universe  # Return the number of imaginary universes
    
    def set_img_univ(self, delta):
        self.img_universe = delta

    def reset_img_univ(self):
        """Reset the universe value to 0."""
        self.img_universe = self.universes


    # Takes a separate coordinate and returns the distance between the two in coordinate form
    def calculate_distance(self, ref_coordinate):
        # Convert the internal coordinate to its total base10 equivalent
        curr_cord = self.baseTenConv()

        # Check if ref_coordinate is a list and convert it using baseTenConv
        if isinstance(ref_coordinate, list):
            next_coord = self.baseTenConv(ref_coordinate)
        else:
            # Assuming ref_coordinate is an instance of Coordinate
            next_coord = ref_coordinate.baseTenConv()

        # Calculate the distance and convert it to coordinate format
        distance_base_10 = next_coord - curr_cord
        return self.coord_conv(distance_base_10)
    
    #Function takes a 'distance' in base 10 and returns a coordinate object + the distance
    def calculate_final_coordinate(self, distance):
        # Convert the current coordinate to base 10, add the distance, and convert back
        current_base10 = self.coordinate.baseTenConv()
        final_base10 = current_base10 + distance
        return self.coordinate.coord_conv(final_base10)
        



class FractionalCoordinate(Coordinate):
    def __init__(self):
        super().__init__()
        self.coordinates = [0.0] * 5  # Override to use floats
        self.universes = 0  # Keep track of universes (overflows)

    def copy(self):
        new_coordinate = FractionalCoordinate()
        new_coordinate.coordinates = self.coordinates[:]
        new_coordinate.universes = self.universes
        return new_coordinate

    # Override increment methods to handle floats
    def increment_by(self, delta):
        self._update_coordinates(delta)

    def decrement_by(self, delta):
        self._update_coordinates(-delta)

    def _update_coordinates(self, delta):
        total = delta
        for i in range(len(self.coordinates)):
            total += self.coordinates[i]
            self.coordinates[i] = total % 60
            total = total // 60  # Use floor division to keep total as float
        if total >= 1:
            self.universes += int(total)

    # Override baseTenConv to handle floats
    def baseTenConv(self, digits=None):
        if digits is None:
            digits = self.coordinates
        return sum(d * (60 ** i) for i, d in enumerate(digits))

    # Override get_coordinates to display floats
    def get_coordinates(self):
        # Returns the coordinates in a formatted string with up to five decimal places
        return ' '.join(f"{c:.5f}" for c in self.coordinates)

    # Override other methods as needed
    def parse_coordinate(self, coord_str):
        # Modify to handle fractional coordinates
        if '.' in coord_str:
            integer_part_str, fractional_part_str = coord_str.strip().split('.')
            integer_parts = integer_part_str.strip().split()
            fractional_parts = fractional_part_str.strip().split()
            if len(integer_parts) != 5 or len(fractional_parts) != 5:
                raise ValueError("Invalid coordinate format. Expected 5 integer and 5 fractional numbers.")
            integer_parts = [int(x) for x in integer_parts]
            fractional_parts = [float(x) for x in fractional_parts]
            self.coordinates = [i + f / 60 for i, f in zip(integer_parts, fractional_parts)]
        else:
            # Use the parent class method for integer coordinates
            self.coordinates = [float(c) for c in super().parse_coordinate(coord_str)]
        return self.coordinates

    def coord_conv(self, number):
        # Convert a base-10 number to coordinates with floats
        digits = []
        for _ in range(5):
            digits.append(number % 60)
            number //= 60
        digits.reverse()
        self.coordinates = digits
        return self.coordinates