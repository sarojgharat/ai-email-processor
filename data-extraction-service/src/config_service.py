import json
from typing import List, Optional


class ConfigService:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self._data = self._load_config()

    def _load_config(self) -> dict:
        """Load JSON config into memory."""
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_value(self, business_process: str, value_type: str) -> Optional[str]:
        """
        Retrieve a list of strings for the given business_process and type.

        :param business_process: e.g., "booking" or "equipment"
        :param value_type: e.g., "categories" or "rules"
        :return: List of strings if found, else None
        """
        process_config = self._data.get(business_process.lower())
        if not process_config:
            return None

        value = process_config.get(value_type)
        if not value:
            return None

        return value

if __name__ == "__main__":
    service = ConfigService("src\\config.json")

    # Example usage
    print(service.get_value("booking", "booking request"))  
    # -> ["New Booking", "Amendment", "Cancellation"]

    print(service.get_value("equipment", "equipment release request"))  
    # -> ["Depot must be valid", "Check container type", "Verify pickup date"]
