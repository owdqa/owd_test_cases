#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
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
        self.contacts = Contacts(self)
        self.messages = Messages(self)

        #
        # Import contact (adjust the correct number).
        #
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        self.messages.launch()

        #
        # Start a new SMS and add the message and contact name.
        #
        self.messages.startNewSMS()
        self.messages.selectAddContactButton()
        self.contacts.view_contact(self.contact["familyName"], False)
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        self.messages.checkIsInToField(self.contact["name"], True)

        #
        # Remove it.
        #
        self.messages.removeContactFromToField(self.contact["name"])

        #
        # Verify the contact name is present before removing it.
        #
        self.messages.checkIsInToField(self.contact["name"], False)
