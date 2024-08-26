import json
from typing import Dict
from ..models.containers import ContainerDataModel


class ContainerDataFactory:
    def __init__(self, mapping_file: str = "mappings.json"):
        # Load the mapping configuration from the JSON file
        self.mapping_config = self._load_mappings(mapping_file)

    @staticmethod
    def _load_mappings(mapping_file: str) -> Dict[str, Dict[str, str]]:
        """
        Load the mappings from the specified JSON file.
        """
        try:
            with open(mapping_file, 'r') as f:
                return json.load(f).get("scrapers", {})
        except FileNotFoundError:
            raise ValueError(f"Mapping file {mapping_file} not found.")
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Error decoding JSON from {mapping_file}: {str(e)}")

    def create_container_data(self, scraper_name: str, row: Dict[str, str]) -> ContainerDataModel:
        """
        Create a ContainerDataModel instance based on the scraper name and data row.
        """
        mapping = self.mapping_config.get(scraper_name)
        if not mapping:
            raise ValueError(f"No mapping found for scraper: {scraper_name}")

        data = {
            model_field: row.get(raw_field)
            for model_field, raw_field in mapping.items()
        }
        return ContainerDataModel(**data)
