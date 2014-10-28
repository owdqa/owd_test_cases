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
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.contacts import MockContact


class main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.settings = Settings(self)
        self.test_contact = MockContact()
        self.fxa_user = self.UTILS.general.get_os_variable("GLOBAL_FXA_USER")
        self.fxa_pass = self.UTILS.general.get_os_variable("GLOBAL_FXA_PASS")

        self.test_contact["email"] = ""
        self.test_contact["tel"] = ""
        self.UTILS.general.insertContact(self.test_contact)

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

            self.UTILS.iframe.switch_to_active_frame()
            elem = (DOM.Loop.call_screen_contact_details[
                    0], DOM.Loop.call_screen_contact_details[1].format(self.test_contact["name"]))
            self.UTILS.element.waitForElements(elem, "Call to contact: {}".format(self.test_contact["name"]))

            self.UTILS.element.waitForElements(
                DOM.Loop.share_panel, "When we call a contact with no number or email, a fallback mechanism is shown")
