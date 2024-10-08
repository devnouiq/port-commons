from typing import Dict, List
from commons.schemas.shipment import ContainerAvailability
from commons.rules.engine import BusinessRule


class ContainerDataFactory:
    def __init__(self, mapping_config: Dict[str, str], rules: List[BusinessRule] = None):
        """
        Initialize the factory with the mapping configuration and custom rules.
        :param mapping_config: A dictionary containing the mapping configuration.
        :param rules: A list of rules to apply for computing complex values.
        """
        self.mapping_config = mapping_config
        self.rules = rules or []

    def create_container_data(self, row: Dict[str, str], shipment_id: int) -> ContainerAvailability:
        """
        Create a ContainerAvailability instance based on the provided data row.
        :param row: A dictionary representing a row of data from the scraper.
        :param shipment_id: The ID of the shipment associated with this container.
        :return: A ContainerAvailability instance.
        """
        # Step 1: Map the data from the JSON using the mapping configuration
        mapped_data = {
            field: row.get(source_field)
            for field, source_field in self.mapping_config.items()
        }

        # Step 2: Apply the custom rules to compute or override values in the mapped data
        for rule_class in self.rules:
            rule_instance = rule_class(json_data=row, mapped_data=mapped_data)
            rule_instance.process()

        # Step 3: Filter the mapped_data to only include fields relevant to ContainerAvailability
        relevant_data = {field: value for field, value in mapped_data.items(
        ) if hasattr(ContainerAvailability, field)}

        # Step 4: Capture non-relevant fields in `additional_info`
        additional_info = {field: value for field,
                           value in mapped_data.items() if field not in relevant_data}

        # Step 5: Create and return the ContainerAvailability object with the relevant mapped data and additional info
        container_availability = ContainerAvailability(
            shipment_id=shipment_id,
            additional_info=additional_info,  # Store the additional data
            **relevant_data
        )

        return container_availability
