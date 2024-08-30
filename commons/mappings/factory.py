from typing import Dict
from ..models.containers import ContainerDataModel


class ContainerDataFactory:
    def __init__(self, mapping_config: Dict[str, str]):
        """
        Initialize the factory with the mapping configuration.
        :param mapping_config: A dictionary containing the mapping configuration.
        """
        self.mapping_config = mapping_config

    def create_container_data(self, row: Dict[str, str], shipment_id: int) -> ContainerDataModel:
        """
        Create a ContainerAvailability instance based on the provided data row.
        :param row: A dictionary representing a row of data from the scraper.
        :param shipment_id: The ID of the shipment associated with this container.
        :return: A ContainerAvailability instance.
        """
        # Map the data from the JSON using the mapping configuration
        mapped_data = {
            field: str(row.get(source_field)) if isinstance(
                row.get(source_field), bool) else row.get(source_field)
            for field, source_field in self.mapping_config.items()
        }

        # Create and return the ContainerAvailability object
        container_availability = ContainerDataModel(
            shipment_id=shipment_id,
            **mapped_data
        )
        return container_availability
