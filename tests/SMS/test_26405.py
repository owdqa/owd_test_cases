#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)
        self.contact = MockContact(tel=[{'type': 'Mobile', 'value': '11111111'},
                                    {'type': 'Mobile', 'value': '222222222'}])

        #
        # We're not testing adding a contact, so just stick one
        # into the database.
        #
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Type a message containing the required string
        #
        self.messages.startNewSMS()
        self.messages.enterSMSMsg("Test message")

        #
        # Search for our contact.
        #
        self.messages.selectAddContactButton()
        self.contacts.search(self.contact['name'])
        self.contacts.select_search_result_several_phones(self.contact['name'], 0)
