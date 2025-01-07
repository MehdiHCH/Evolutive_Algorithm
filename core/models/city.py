import math
from typing import List, Optional, TextIO
from dataclasses import dataclass
from pathlib import Path

@dataclass
class City:
    """
    Represents a city with an identifier and coordinates.
    
    Attributes:
        ID: Unique identifier for the city
        x: X-coordinate of the city
        y: Y-coordinate of the city
    """
    ID: int
    x: float
    y: float

    @classmethod
    def create_city(cls, ID: int, x: float, y: float) -> 'City':
        """
        Creates a new city with the specified identifier and coordinates.
        
        Args:
            ID: Unique identifier for the city
            x: X-coordinate of the city
            y: Y-coordinate of the city
            
        Returns:
            A new City instance
        """
        return cls(ID=ID, x=x, y=y)

    def distance(self, other_city: 'City') -> float:
        """
        Calculates the Euclidean distance between this city and another.
        
        Args:
            other_city: The city to calculate distance to
            
        Returns:
            The Euclidean distance between the cities
        """
        return math.sqrt((self.x - other_city.x) ** 2 + (self.y - other_city.y) ** 2)

    def manhattan_distance(self, other_city: 'City') -> float:
        """
        Calculates the Manhattan distance between this city and another.
        
        Args:
            other_city: The city to calculate distance to
            
        Returns:
            The Manhattan distance between the cities
        """
        return abs(self.x - other_city.x) + abs(self.y - other_city.y)

    def is_equal(self, other_city: 'City') -> bool:
        """
        Compares two cities to determine if they are identical.
        
        Args:
            other_city: The city to compare with
            
        Returns:
            True if the cities are identical, False otherwise
        """
        return (self.ID == other_city.ID and
                self.x == other_city.x and
                self.y == other_city.y)

    def __eq__(self, other: object) -> bool:
        """
        Implements equality comparison for cities.
        
        Args:
            other: The object to compare with
            
        Returns:
            True if the cities are equal, False otherwise
        """
        if not isinstance(other, City):
            return False
        return self.is_equal(other)

    def __hash__(self) -> int:
        """
        Implements hash function for cities.
        
        Returns:
            Hash value based on ID and coordinates
        """
        return hash((self.ID, self.x, self.y))

    def __str__(self) -> str:
        """
        Returns a string representation of the city.
        
        Returns:
            String representation based on the city's ID
        """
        return str(self.ID)

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the city.
        
        Returns:
            Detailed string representation including coordinates
        """
        return f"City(ID={self.ID}, x={self.x:.2f}, y={self.y:.2f})"

    @staticmethod
    def display_cities(cities: List['City']) -> None:
        """
        Displays a list of cities.
        
        Args:
            cities: List of cities to display
        """
        print(" ".join(str(city) for city in cities))

    @staticmethod
    def display_cities_detailed(cities: List['City']) -> None:
        """
        Displays a detailed list of cities including coordinates.
        
        Args:
            cities: List of cities to display
        """
        for city in cities:
            print(f"City {city.ID}: ({city.x:.2f}, {city.y:.2f})")

    @staticmethod
    def read_cities_from_file(file_path: str) -> List['City']:
        """
        Reads city data from a file and returns a list of cities.
        The file should contain:
        - First line: number of cities
        - Following lines: ID x y
        
        Args:
            file_path: Path to the file containing city data
            
        Returns:
            List of City objects, empty list if there's an error
            
        Raises:
            ValueError: If the file format is invalid
            FileNotFoundError: If the file doesn't exist
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        cities = []
        try:
            with path.open('r') as file:
                cities = City._parse_city_file(file)
        except ValueError as e:
            raise ValueError(f"Invalid file format: {str(e)}")
        
        return cities

    @staticmethod
    def _parse_city_file(file: TextIO) -> List['City']:
        """
        Parses city data from an open file.
        
        Args:
            file: Open file object containing city data
            
        Returns:
            List of City objects
            
        Raises:
            ValueError: If the file format is invalid
        """
        try:
            num_cities = int(file.readline().strip())
            cities = []

            for _ in range(num_cities):
                line = file.readline().strip()
                if not line:
                    raise ValueError("Unexpected end of file")
                
                parts = line.split()
                if len(parts) != 3:
                    raise ValueError(f"Invalid line format: {line}")
                
                try:
                    ID = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    cities.append(City.create_city(ID, x, y))
                except ValueError:
                    raise ValueError(f"Invalid number format in line: {line}")

            return cities

        except Exception as e:
            raise ValueError(f"Error parsing file: {str(e)}")

    @staticmethod
    def save_cities_to_file(cities: List['City'], file_path: str) -> None:
        """
        Saves a list of cities to a file.
        
        Args:
            cities: List of cities to save
            file_path: Path where to save the file
            
        Raises:
            IOError: If there's an error writing to the file
        """
        path = Path(file_path)
        
        try:
            with path.open('w') as file:
                file.write(f"{len(cities)}\n")
                for city in cities:
                    file.write(f"{city.ID} {city.x} {city.y}\n")
        except IOError as e:
            raise IOError(f"Error writing to file: {str(e)}")

    def to_dict(self) -> dict:
        """
        Converts the city to a dictionary representation.
        
        Returns:
            Dictionary containing the city's data
        """
        return {
            'id': self.ID,
            'x': self.x,
            'y': self.y
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'City':
        """
        Creates a city from a dictionary representation.
        
        Args:
            data: Dictionary containing city data
            
        Returns:
            A new City instance
        """
        return cls(
            ID=data['id'],
            x=data['x'],
            y=data['y']
        )