from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        #
        # Get details of our test contacts.
        #
        self.contact = MockContact(tel={'type': 'Mobile', 'value': '+345555555555'})
        self.UTILS.general.insertContact(self.contact)

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
        self.contacts.view_contact(self.contact["name"])

        #
        # Tap the phone number.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.view_contact_tel_field, "Telephone number")
        x.tap()

        #
        # Switch to dialer.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)

        self.UTILS.element.waitForElements(("xpath", DOM.Dialer.outgoing_call_numberXP.format(self.contact["name"])),
                                    "Outgoing call found with number matching {}".format(self.contact["name"]))

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of contact:", x)
