from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact
import time


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        # Get details of our test contacts.
        self.test_contact = MockContact()
        self.UTILS.general.insertContact(self.test_contact)

        self.contact_name = self.test_contact["givenName"]

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()
        contacts_option_btn = self.UTILS.element.getElement(DOM.Dialer.option_bar_contacts, "Contacts option")
        contacts_option_btn.tap()
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.contacts_sub_iframe, via_root_frame=False)

        self.contacts.view_contact(self.contact_name, header_check=False)
        phone_field = self.UTILS.element.getElement(DOM.Contacts.view_contact_tel_field, "Telephone number")
        phone_field.tap()

        # The call is tested.
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.UTILS.element.waitForElements(("xpath", DOM.Dialer.outgoing_call_numberXP.format(self.test_contact["name"])),
                                           "Outgoing call found with number matching {}".format(self.test_contact["name"]))
        self.dialer.hangUp()
