# OWD-35077: Verify that it is possible to select a contact from the Address Book.

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
        self.fxa_user = self.UTILS.general.get_config_variable("GLOBAL_FXA_USER")
        self.fxa_pass = self.UTILS.general.get_config_variable("GLOBAL_FXA_PASS")
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
            self.UTILS.element.waitForElements(elem, "Contact in address book")