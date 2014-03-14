#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.apps.contacts import Contacts

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContact
from tests.CONTACTS.shared_test_functions import test_field_remove_toggle


class test_main(test_field_remove_toggle):

    def test_run(self):
        contact = MockContact()
        self.field_remove_toggle_test(contact, "thumbnail-action")
