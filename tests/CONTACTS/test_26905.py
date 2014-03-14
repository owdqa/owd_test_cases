#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact
from tests.CONTACTS.shared_test_functions import test_field_remove_toggle


class test_main(test_field_remove_toggle):

    def test_run(self):
        contact = MockContact(tel=[{'type': 'Mobile', 'value': '555555555'},
                                   {'type': 'Mobile', 'value': '666666666'},
                                   {'type': 'Mobile', 'value': '777777777'}])
        self.field_remove_toggle_test(contact, "contacts-form-phones", [0, 1, 2])
