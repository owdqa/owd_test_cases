from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
import time
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        # Get details of our test contacts.
        self.contact = MockContact(tel=[{'type': 'Mobile', 'value': '555555555'},
                                        {'type': 'Mobile', 'value': '666666666'}])
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Launch contacts app.
        self.contacts.launch()

        # View our contact.
        self.contacts.view_contact(self.contact['name'])

        # Tap the 2nd number to dial it.
        x = self.UTILS.element.getElement(("xpath", DOM.Contacts.view_contact_tels_xpath.\
                                    format(self.contact["tel"][1]["value"])), "Second phone number")
        x.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)

        # Verify things....
        time.sleep(0.5)
        self.UTILS.element.getElements(DOM.Dialer.outgoing_call_locator, "Outgoing Call in progress")

        outgoing_number = self.UTILS.element.getElement(DOM.Dialer.outgoing_call_number, "Outgoing number being called")
        self.UTILS.test.test(outgoing_number.text == self.contact["givenName"] + " " + self.contact["familyName"], 
                                        "Outgoing contact being called matches the stored in the address book")

