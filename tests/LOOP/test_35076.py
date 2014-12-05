# OWD-35076: Verify that is possible to start a Loop communication to an entry of the Address Book
import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM
from tests.i18nsetup import setup_translations
from OWDTestToolkit.utils.contacts import MockContact


class main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.settings = Settings(self)
        self.test_contact = MockContact()
        self.fxa_user = self.UTILS.general.get_config_variable("fxa_user", "common")
        self.fxa_pass = self.UTILS.general.get_config_variable("fxa_pass", "common")

        self.connect_to_network()
        self.UTILS.general.insertContact(self.test_contact)
        # Clean start
        if not self.loop.is_installed():
            self.loop.install()
        else:
            self.loop.launch()
            # If already logged in, logout
            if not self.loop.wizard_or_login():
                self.loop.open_settings()
                self.loop.logout()

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
            elem = (DOM.Loop.call_screen_contact_details[0], DOM.Loop.call_screen_contact_details[1].format(self.test_contact["name"]))
            self.UTILS.element.waitForElements(elem, "Call to contact: {}".format(self.test_contact["name"]))