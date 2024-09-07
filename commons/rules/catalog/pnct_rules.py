from typing import Dict


class PnctRules:
    def __init__(self, json_data: Dict[str, str], mapped_data: Dict[str, str]):
        """
        Initialize the rules with the JSON data and the mapped data dictionary.
        :param json_data: The JSON response data from the scraper.
        :param mapped_data: The dictionary containing the mapped data.
        """
        self.json_data = json_data
        self.mapped_data = mapped_data

    def apply_available_rule(self):
        """Apply the rule for 'Available'."""
        available_status = self.json_data.get('Available', '')
        self.mapped_data['available'] = 'YES' if available_status == 2 else 'NO'

    def apply_demurrage_rule(self):
        """Apply the rule for 'Demurrage'."""
        demurrage_amount = self.json_data.get('DemurrageAmount', 0)
        if demurrage_amount > 0:
            self.mapped_data['demurrage_amount'] = 'YES'
        else:
            self.mapped_data['demurrage_amount'] = 'NO'

    def apply_charges_fees_rule(self):
        """Apply the rule for 'Charges/fees'."""
        terminal_demurrage_amt = self.json_data.get('DemurrageAmount', 0)
        non_demurrage_amt = self.json_data.get('LineDemurrageAmount', 0)
        total_charges = terminal_demurrage_amt + non_demurrage_amt
        self.mapped_data['charges'] = total_charges

    def apply_holds_rule(self):
        """Apply the rule for 'Holds (Y/N)'."""
        customs_status = self.json_data.get('CustomReleaseStatus', '')
        freight_status = self.json_data.get('CarrierReleaseStatus', '')
        misc_hold_status = self.json_data.get('MiscHoldStatus', '')

        if customs_status == 'HOLD' or freight_status == 'HOLD' or misc_hold_status == 'HOLD':
            self.mapped_data['holds'] = 'YES'
        else:
            self.mapped_data['holds'] = 'NO'

    def apply_type_code_rule(self):
        """Apply the rule for 'Type Code'."""
        self.mapped_data['type_code'] = self.json_data.get(
            'SizeTypeHeight', '')

    def apply_all_rules(self):
        """Apply all the rules to the mapped_data object."""
        self.apply_available_rule()
        self.apply_demurrage_rule()
        self.apply_charges_fees_rule()
        self.apply_holds_rule()
        self.apply_type_code_rule()
