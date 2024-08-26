from typing import Dict
from ..models.containers import ContainerDataModel


class ContainerDataFactory:
    def __init__(self, mapping_config: Dict[str, str]):
        """
        Initialize the factory with the mapping configuration.
        :param mapping_config: A dictionary containing the mapping configuration.
        """
        self.mapping_config = mapping_config

    def create_container_data(self, row: Dict[str, str]) -> ContainerDataModel:
        """
        Create a ContainerDataModel instance based on the provided data row.
        :param row: A dictionary representing a row of data from the scraper.
        :return: A ContainerDataModel instance.
        """
        data = {
            model_field: row.get(raw_field)
            for model_field, raw_field in self.mapping_config.items()
        }
        return ContainerDataModel(**data)
