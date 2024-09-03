from datetime import datetime, timezone
from typing import Dict


class PTPRules:
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
        status = self.json_data.get('Status', '')
        if status == 'ON VESSEL':
            self.mapped_data['available'] = 'NO'
        elif status == 'IN YARD':
            hold_fields = [
                self.json_data.get('Freight', ''),
                self.json_data.get('Customs', ''),
                self.json_data.get('Hold', '')
            ]
            self.mapped_data['available'] = 'YES' if not any(
                hold == 'HOLD' for hold in hold_fields) else 'NO'

    def apply_demurrage_rule(self):
        """Apply the rule for 'Demurrage'."""
        current_date = self.json_data.get('LocalDateTime', '')
        good_thru = self.json_data.get('GoodThru', '')
        carrier_status = self.json_data.get('CarrierStatus', 'N/A')
        if current_date > good_thru and carrier_status == 'N/A':
            self.mapped_data['demurrage_amount'] = 'YES'
        else:
            self.mapped_data['demurrage_amount'] = 'NO'

    def apply_holds_rule(self):
        """Apply the rule for 'Holds'."""
        if self.json_data.get('Customs', '') == 'HOLD' or \
           self.json_data.get('Freight', '') == 'HOLD' or \
           self.json_data.get('Hold', '') == 'HOLD':
            self.mapped_data['holds'] = 'YES'
        else:
            self.mapped_data['holds'] = 'NO'

    def apply_departed_terminal_rule(self):
        """Apply the rule for 'Departed Terminal'."""
        if self.json_data.get('DepartureCarrier', 'N/A') != 'N/A':
            self.mapped_data['yard_terminal_release_status'] = 'YES'
        else:
            self.mapped_data['yard_terminal_release_status'] = 'NO'

    def apply_transit_state_rule(self):
        """Apply the rule for 'Transit State'."""
        self.mapped_data['transit_state'] = self.json_data.get('Status', 'N/A')

    # Adding new rules based on the original `container_data` logic

    def apply_usda_status_rule(self):
        """Apply the rule for 'USDA Status'."""
        self.mapped_data['usda_status'] = next(
            (hold.get('status', 'N/A') for hold in self.json_data.get('shipmentstatus', [{}])[0].get('holdsinfo', [{}]) if hold.get('type') == 'CUSTOMS'), 'N/A')

    def apply_last_free_date_rule(self):
        """Apply the rule for 'Last Free Date'."""
        self.mapped_data['last_free_date'] = self.json_data.get(
            'locations', [{}])[0].get('locationinfo', {}).get('currentconditioninfo', {}).get('lastfree_dttm', 'N/A')

    def apply_location_rule(self):
        """Apply the rule for 'Location'."""
        self.mapped_data['location'] = self.json_data.get(
            'locations', [{}])[0].get('locationinfo', {}).get('currentconditioninfo', {}).get('yard_loc', 'N/A')

    def apply_custom_release_status_rule(self):
        """Apply the rule for 'Custom Release Status'."""
        self.mapped_data['custom_release_status'] = next(
            (hold.get('status', 'N/A') for hold in self.json_data.get('shipmentstatus', [{}])[0].get('holdsinfo', [{}]) if hold.get('type') == 'CUSTOMS'), 'N/A')

    def apply_carrier_release_status_rule(self):
        """Apply the rule for 'Carrier Release Status'."""
        self.mapped_data['carrier_release_status'] = next(
            (hold.get('status', 'N/A') for hold in self.json_data.get('shipmentstatus', [{}])[0].get('holdsinfo', [{}]) if hold.get('type') == 'FREIGHT'), 'N/A')

    def process(self):
        """
        Apply all the rules to the mapped_data object.
        """
        self.apply_available_rule()
        self.apply_demurrage_rule()
        self.apply_holds_rule()
        self.apply_departed_terminal_rule()
        self.apply_transit_state_rule()
        # Apply new rules
        self.apply_usda_status_rule()
        self.apply_last_free_date_rule()
        self.apply_location_rule()
        self.apply_custom_release_status_rule()
        self.apply_carrier_release_status_rule()
