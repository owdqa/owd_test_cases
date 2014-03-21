#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        #
        # Prepare the contact we're going to insert.
        #
        self.num1 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel={'type': '', 'value': self.num1})

        self.UTILS.general.insertContact(self.contact)
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact["tel"]["value"])

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Type a message containing the required string
        #
        self.messages.startNewSMS()
        self.messages.enterSMSMsg("Test message")

        #
        # Search for our contact.
        #
        self.messages.selectAddContactButton()
        self.contacts.search("Knot A Match")
        self.contacts.check_search_results("Knot A Match", False)
