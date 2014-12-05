# OWD-35078: Verify that it is possible to use a search tool to find the desired contact
import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit import DOM
from tests.i18nsetup import setup_translations
from OWDTestToolkit.utils.contacts import MockContact


class main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)
        self.fxa_user = self.UTILS.general.get_config_variable("fxa_user", "common")
        self.fxa_pass = self.UTILS.general.get_config_variable("fxa_pass", "common")

        self.connect_to_network()

        self.target_name = "QA"
        self.test_contacts = [MockContact() for i in range(5)]
        self.test_contacts[0]["givenName"] = self.target_name
        self.test_contacts[0]["familyName"] = "Automation"
        map(self.UTILS.general.insertContact, self.test_contacts)

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
            self.contacts.search(self.target_name)
            self.contacts.check_search_results(self.target_name)