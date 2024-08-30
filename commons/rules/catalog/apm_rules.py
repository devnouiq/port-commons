from typing import Dict


class APMRules:
    def __init__(self, mapped_data: Dict[str, str]):
        """
        Initialize the rules with the mapped data.
        :param mapped_data: The mapped data from the factory.
        """
        self.mapped_data = mapped_data

    def apply_demurrage_rule(self):
        """Apply the rule for 'Demurrage'."""
        current_date = self.mapped_data.get('LocalDateTime', '')
        gate_out_date = self.mapped_data.get('GateOutDate', '')
        good_thru = self.mapped_data.get('GoodThru', '')

        if current_date > good_thru and not gate_out_date:
            self.mapped_data['Demurrage'] = 'YES'
        else:
            self.mapped_data['Demurrage'] = 'NO'

    def apply_holds_rule(self):
        """Apply the rule for 'Holds'."""
        freight_status = self.mapped_data.get('freight', '')
        customs_status = self.mapped_data.get('customs', '')
        hold = self.mapped_data.get('Hold', '')

        if freight_status == 'HOLD' or customs_status == 'HOLD' or hold == 'HOLD':
            self.mapped_data['Holds'] = 'YES'
        else:
            self.mapped_data['Holds'] = 'NO'

    def apply_transit_state_rule(self):
        """Apply the rule for 'Transit State'."""
        if not self.mapped_data.get('YardLocation'):
            self.mapped_data['transit_state'] = self.mapped_data.get(
                'VesselEta', '')

    def process(self, mapped_data: Dict[str, str]) -> Dict[str, str]:
        """
        Apply all the rules to modify the mapped data before creating ContainerAvailability.
        :param mapped_data: The mapped data dictionary.
        :return: The modified mapped data dictionary.
        """
        self.mapped_data = mapped_data

        self.apply_demurrage_rule()
        self.apply_holds_rule()
        self.apply_transit_state_rule()
        return self.mapped_data
