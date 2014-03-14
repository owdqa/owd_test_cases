#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Create our test contacts.
        #
        self.contact_list = [MockContact(tel={'type': 'Mobile', 'value': "{}".format(i) * 9}) for i in range(3)]
        map(self.UTILS.insertContact, self.contact_list)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Search for our new contact.
        #
        self.contacts.search("999999999")

        #
        # Verify that there are no results.
        #
        self.UTILS.waitForElements(DOM.Contacts.search_no_contacts_found, "'No contacts found' message")
