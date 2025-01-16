from typing import Dict, List, Any
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

    def create_container_data(self, row: Dict[str, Any], shipment_id: int) -> ContainerAvailability:
        """
        Create a ContainerAvailability instance based on the provided data row.
        :param row: A dictionary representing a row of data from the scraper.
        :param shipment_id: The ID of the shipment associated with this container.
        :return: A ContainerAvailability instance.
        """
        # -- STEP A: Copy the entire row so we can track fields not mapped at all.
        unmapped_fields = dict(row)

        # -- STEP B: Build mapped_data from mapping_config
        mapped_data = {}
        for target_field, source_field in self.mapping_config.items():
            value = row.get(source_field)
            mapped_data[target_field] = value

            # If the source_field existed in 'row', remove it from unmapped_fields.
            if source_field in unmapped_fields:
                del unmapped_fields[source_field]

        # -- STEP C: Apply custom rules to compute/override fields in mapped_data
        for rule_class in self.rules:
            rule_instance = rule_class(json_data=row, mapped_data=mapped_data)
            rule_instance.process()

        # -- STEP D: Determine which mapped_data fields belong on ContainerAvailability
        relevant_data = {}
        leftover_mapped = {}
        for field_name, field_value in mapped_data.items():
            if hasattr(ContainerAvailability, field_name):
                relevant_data[field_name] = field_value
            else:
                leftover_mapped[field_name] = field_value

        # -- STEP E: Combine leftover_mapped + unmapped_fields into additional_info
        additional_info = {}
        additional_info.update(leftover_mapped)
        additional_info.update(unmapped_fields)

        # *Remove fields with value=None in additional_info*
        additional_info = {
            k: v for k, v in additional_info.items() if v is not None
        }

        # -- STEP F: Build and return the ContainerAvailability object
        container_availability = ContainerAvailability(
            shipment_id=shipment_id,
            additional_info=additional_info,
            **relevant_data
        )

        return container_availability