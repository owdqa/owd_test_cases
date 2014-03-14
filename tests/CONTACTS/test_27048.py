#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
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

        #
        # Launch contacts app.
        #
        self.contacts.launch()
        x = self.contacts.import_hotmail_login("wrongname", "wrongpass")
        self.UTILS.TEST(x == False, "Login failed.")
