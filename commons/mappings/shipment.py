from typing import Any, Dict, List
from commons.rules.engine import BusinessRule


class ShipmentDataFactory:
    def __init__(self, config: Dict[str, bool] = None, rules: List[BusinessRule] = None):
        """
        Initialize the factory with custom rules for Shipments and a config.
        :param rules: A list of rules to apply for updating fields in the shipment.
        :param config: A dictionary with configuration flags to determine which rules to apply.
        """
        self.rules = rules or []

    def create_shipment_data(self, row: Dict[str, str], shipment: Any) -> None:
        """
        Apply rules and update specific fields in the existing Shipment object based on config flags.
        :param row: A dictionary representing a row of data from the scraper.
        :param shipment: The existing Shipment object to be updated.
        """
        # Step 1: Apply the custom rules to compute or override values based on config
        for rule_class in self.rules:
            rule_instance = rule_class(
                json_data=row, shipment=shipment
            )
            rule_instance.process()
