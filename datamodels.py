import hashlib
from dataclasses import dataclass
from datetime import date


@dataclass
class TourInfo:
    country: str
    leader: str
    days: int
    start_date: date
    end_date: date
    price: float
    discount: int
    is_available: bool

    def __hash__(self):
        # Combine attributes into a single string representation
        data = f"{self.country}|{self.days}|{self.start_date}|{self.end_date}|{self.price}|{self.discount}"
        # Create a stable hash using SHA-256
        return int(hashlib.sha256(data.encode("utf-8")).hexdigest(), 16)


def print_color(text: str, color: str):
    # ANSI escape codes for colors
    line_color = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "light blue": "\033[96m",
    }.get(
        color, ""
    )  # Default to no color if the color is not found
    reset = "\033[0m"  # Reset to default
    print(f"{line_color}{text}{reset}")
