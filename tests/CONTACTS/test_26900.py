#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
import time

#
# Imports particular to this test case.
#
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
        # Get details of our test contacts.
        #
        self.contact = MockContact(tel=[{'type': 'Mobile', 'value': '555555555'},
                                        {'type': 'Mobile', 'value': '666666666'}])
        self.UTILS.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # View our contact.
        #
        self.contacts.view_contact(self.contact['name'])

        #
        # Tap the 2nd number to dial it.
        #
        x = self.UTILS.getElement(("xpath", DOM.Contacts.view_contact_tels_xpath.\
                                    format(self.contact["tel"][1]["value"])), "Second phone number")
        x.tap()

        #
        # Switch to the dialer iframe.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.dialer_frame)

        #
        # Verify things....
        #
        time.sleep(0.5)
        x = self.UTILS.getElements(DOM.Dialer.outgoing_call_locator, "Outgoing Call in progress")
