#===============================================================================
# 27060: Type a two digits number and check the list of contacts shown
#
# Pre-requisites:
# To have several contacts stored on the Address Book List any of them
# matching the number introduced
#
# Procedure:
# 1. Open Contacts app
# 2. Tap on Search box
# 3. Insert two numbers
#
# Expected results:
# The contacts whose phone's numbers have the numbers inserted are displayed
#===============================================================================

import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Get details of our test contacts.
        #
        self.phones = ["198111111", "198222222", "133333333"]

        self.test_contacts = [MockContact(tel={'type': 'Mobile', 'value': self.phones[i]})\
                                for i in range(3)]
        map(self.UTILS.general.insertContact, self.test_contacts)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Search for our new contact.
        #
        self.contacts.search("98")

        #
        # Verify our contact is listed.
        #
        conditions = [True, True, False]
        names = [c["givenName"] for c in self.test_contacts]
        map(self.contacts.check_search_results, names, conditions)
