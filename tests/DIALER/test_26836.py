import sys
sys.path.insert(1, "./")

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact
from tests.i18nsetup import setup_translations


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        # Get details of our test contacts.
        self.Contact_1 = MockContact()
        self.UTILS.general.insertContact(self.Contact_1)
        _ = setup_translations(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.toggleViaStatusBar("airplane")

        # Launch contacts app.
        self.contacts.launch()

        # Search for our new contact.
        self.contacts.view_contact(self.Contact_1["name"])

        # Tap the phone number.
        phone_field = self.UTILS.element.getElement(DOM.Contacts.view_contact_tel_field, "Telephone number")
        phone_field.tap()

        # Switch to dialer.
        warning_header = (DOM.GLOBAL.confirmation_msg_header[0],
                          DOM.GLOBAL.confirmation_msg_header[1].format(_("Airplane mode activated")))

        self.UTILS.element.getElement(warning_header, "Airplane mode warning [header]")
        ok_btn = self.UTILS.element.getElement(DOM.GLOBAL.confirmation_msg_ok_btn, "OK button")
        ok_btn.tap()

        self.UTILS.element.waitForElements(DOM.Contacts.view_details_title, "Contact details")
