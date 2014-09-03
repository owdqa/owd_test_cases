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

    test_msg = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)

        #
        # Prepare the contact we're going to insert.
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(givenName = '', familyName = '', name = '', tel = {'type': '', 'value': self.phone_number})

        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Clear out any current messages.
        #
        self.messages.launch()

        #
        # Create SMS.
        #
        self.messages.startNewSMS()
        self.messages.addNumbersInToField([ self.contact["tel"]["value"] ])
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Click send.
        #
        self.messages.sendSMS()

        #
        # Wait for the last message in this thread to be a 'received' one.
        #
        self.messages.waitForReceivedMsgInThisThread()

        #
        # Verify the number is shown in the header as there is no contact name
        #
        self.messages.checkThreadHeader(str(self.contact["tel"]["value"]))
