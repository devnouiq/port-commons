from typing import Dict
from commons.schemas.shipment import ContainerAvailability


class APMRules:
    def __init__(self, json_data: Dict[str, str], mapped_data: Dict[str, str]):
        """
        Initialize the rules with the JSON data and the mapped data dictionary.
        :param json_data: The JSON response data from the scraper.
        :param mapped_data: The dictionary containing the mapped data.
        """
        self.json_data = json_data
        self.mapped_data = mapped_data

    def apply_demurrage_rule(self):
        """Apply the rule for 'Demurrage'."""
        current_date = self.json_data.get('LocalDateTime', '')
        gate_out_date = self.json_data.get('GateOutDate', '')
        good_thru = self.json_data.get('GoodThru', '')

        if current_date > good_thru and not gate_out_date:
            self.mapped_data['demurrage_amount'] = 'YES'
        else:
            self.mapped_data['demurrage_amount'] = 'NO'

    def apply_holds_rule(self):
        """Apply the rule for 'Holds'."""
        freight_status = self.json_data.get('Freight', '')
        customs_status = self.json_data.get('Customs', '')
        hold = self.json_data.get('Hold', '')

        if freight_status == 'HOLD' or customs_status == 'HOLD' or hold == 'HOLD':
            self.mapped_data['holds'] = 'YES'
        else:
            self.mapped_data['holds'] = 'NO'

    def apply_departed_terminal_rule(self):
        """Apply the rule for 'Departed Terminal'."""
        if self.json_data.get('GateOutDate'):
            self.mapped_data['yard_terminal_release_status'] = 'YES'
        else:
            self.mapped_data['yard_terminal_release_status'] = 'NO'

    def apply_transit_state_rule(self):
        """Apply the rule for 'Transit State'."""
        if not self.json_data.get('YardLocation'):
            self.mapped_data['transit_state'] = self.json_data.get(
                'VesselEta', '')

    def process(self):
        """
        Apply all the rules to the mapped_data object.
        """
        self.apply_demurrage_rule()
        self.apply_holds_rule()
        self.apply_departed_terminal_rule()
        self.apply_transit_state_rule()
