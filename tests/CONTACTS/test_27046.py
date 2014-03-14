#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps import Settings
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.gmail_user = self.UTILS.get_os_variable("GMAIL_1_USER")
        self.gmail_passwd = self.UTILS.get_os_variable("GMAIL_1_PASS")

        #
        # Create test contacts.
        #
        self.contact = MockContact()
        self.UTILS.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.UTILS.getNetworkConnection()

        self.contacts.launch()
        self.contacts.import_gmail_login(self.gmail_user, self.gmail_passwd)

        x = self.UTILS.getElements(DOM.Contacts.import_conts_list, "Contact list", True, 20)

        gmail_contacts = []
        for y in x:
            gmail_contacts.append(y.get_attribute("data-search"))

        self.contacts.import_all()
        self.apps.kill_all()
        self.contacts.launch()

        #
        # Check all our contacts are in the list.
        #
        self.UTILS.waitForElements(DOM.Contacts.view_all_contact_JSname, "Name John Smith")

        # ... and the gmail contacts ...
        self.UTILS.waitForElements(DOM.Contacts.view_all_contact_import, "Gmail imported contact")
        self.UTILS.waitForElements(DOM.Contacts.view_all_contact_import2, "Gmail imported contact")

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)
