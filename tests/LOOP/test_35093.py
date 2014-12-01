# OWD-35093: Verify that if the selected contact does not have any e-mail
# or phone number, no connection is established and the user is notified
# of that.

import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.contacts import MockContact
from tests.i18nsetup import setup_translations


class main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.test_contact = MockContact(givenName="QA", familyName="Automation")
        self.fxa_user = self.UTILS.general.get_config_variable("GLOBAL_FXA_USER")
        self.fxa_pass = self.UTILS.general.get_config_variable("GLOBAL_FXA_PASS")
        _ = setup_translations(self)
        self.expected_msg = _("This contact does not have either a phone number or an email address.")

        self.contacts.launch()
        self.contacts.start_create_new_contact()
        cont_fields = self.contacts.get_contact_fields()
        self.contacts.replace_str(cont_fields['givenName'], self.test_contact['givenName'])
        self.contacts.replace_str(cont_fields['familyName'], self.test_contact['familyName'])
        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()

        self.connect_to_network()
        self.loop.initial_test_checks()
        self.settings.launch()
        self.settings.fxa()
        self.settings.fxa_log_out()
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # First, login
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.firefox_login(self.fxa_user, self.fxa_pass)
            self.loop.allow_permission_ffox_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")

            self.loop.open_address_book()
            elem = (DOM.Contacts.view_all_contact_specific_contact[
                    0], DOM.Contacts.view_all_contact_specific_contact[1].format(self.test_contact["givenName"]))
            entry = self.UTILS.element.getElement(elem, "Contact in address book")
            entry.tap()

            time.sleep(5)
            self.marionette.switch_to_frame()
            title = self.UTILS.element.getElement(DOM.GLOBAL.modal_dialog_alert_title, "Error title")
            msg = self.UTILS.element.getElement(DOM.GLOBAL.modal_dialog_alert_msg, "Error message")
            self.UTILS.test.test(title.text == "Firefox Hello", "Error title matches")
            self.UTILS.test.test(msg.text == self.expected_msg, "Error message matches")
