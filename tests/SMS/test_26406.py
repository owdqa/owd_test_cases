from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)

        # Import contact (adjust the correct number).
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.messages.launch()

        # Start a new SMS and add the message and contact name.
        self.messages.startNewSMS()
        self.messages.selectAddContactButton()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.contacts.view_contact(self.contact["givenName"], False)
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        self.messages.checkIsInToField(self.contact["name"], True)

        # Remove it.
        self.messages.removeContactFromToField(self.contact["name"])

        # Verify the contact name is no longer present before removing it.
        self.messages.checkIsInToField(self.contact["name"], False)
