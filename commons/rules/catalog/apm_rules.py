from typing import Dict
from commons.schemas.shipment import ContainerAvailability
from commons.utils.logger import get_logger

logger = get_logger()


class APMRules:
    def __init__(self, json_data: Dict[str, str], container_availability: ContainerAvailability):
        """
        Initialize the rules with the JSON data and the ContainerAvailability instance.
        :param json_data: The JSON response data from the scraper.
        :param container_availability: The ContainerAvailability object to apply the rules to.
        """
        self.json_data = json_data
        self.container_availability = container_availability

    def apply_demurrage_rule(self):
        """Apply the rule for 'Demurrage'."""
        current_date = self.json_data.get('LocalDateTime', '')
        gate_out_date = self.json_data.get('GateOutDate', '')
        good_thru = self.json_data.get('GoodThru', '')

        if current_date > good_thru and not gate_out_date:
            self.container_availability.demurrage_amount = 'YES'
        else:
            self.container_availability.demurrage_amount = 'NO'

    def apply_holds_rule(self):
        """Apply the rule for 'Holds'."""
        freight_status = self.json_data.get('Freight', '')
        customs_status = self.json_data.get('Customs', '')
        hold = self.json_data.get('Hold', '')

        if freight_status == 'HOLD' or customs_status == 'HOLD' or hold == 'HOLD':
            self.container_availability.holds = 'YES'
        else:
            self.container_availability.holds = 'NO'

    def apply_departed_terminal_rule(self):
        """Apply the rule for 'Departed Terminal'."""
        if self.json_data.get('GateOutDate'):
            self.container_availability.yard_terminal_release_status = 'YES'
        else:
            self.container_availability.yard_terminal_release_status = 'NO'

    def apply_transit_state_rule(self):
        """Apply the rule for 'Transit State'."""
        if not self.json_data.get('YardLocation'):
            self.container_availability.transit_state = self.json_data.get(
                'VesselEta', '')

    def process(self):
        """
        Apply all the rules to the container_availability object.
        """
        self.apply_demurrage_rule()
        self.apply_holds_rule()
        self.apply_departed_terminal_rule()
        self.apply_transit_state_rule()
        return self.container_availability
