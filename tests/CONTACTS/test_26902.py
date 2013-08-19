#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContacts
from tests.CONTACTS.shared_test_functions import TEST_FIELD_REMOVE_TOGGLE

class test_main(TEST_FIELD_REMOVE_TOGGLE.main):

    def test_run(self):
        _cont = MockContacts().Contact_1
        self.field_remove_toggle_test(_cont, "thumbnail-action")