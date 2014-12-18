from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact
import time


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        # Get details of our test contacts.
        self.Contact_1 = MockContact()
        self.UTILS.general.insertContact(self.Contact_1)

        self.contact_name = self.Contact_1["givenName"]

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Launch dialer app.
        self.dialer.launch()

        x = self.UTILS.element.getElement(DOM.Dialer.option_bar_contacts, "Contacts option")
        x.tap()

        # Go to the view details screen for this contact.
        self.contacts.view_contact(self.contact_name, header_check=False)

        x = self.UTILS.element.getElement(DOM.Contacts.view_contact_tel_field, "Telephone number")
        x.tap()

        # The call is tested.
        time.sleep(1)
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.UTILS.element.waitForElements(("xpath", DOM.Dialer.outgoing_call_numberXP.format(self.Contact_1["name"])),
                                    "Outgoing call found with number matching {}".format(self.Contact_1["name"]))

        time.sleep(2)

        self.dialer.hangUp()
