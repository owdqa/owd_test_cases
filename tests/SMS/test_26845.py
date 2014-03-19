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
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        #
        # Import contact (adjust to the correct number).
        #
        self.test_num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.cont = MockContact(tel={"type": "Mobile", "value": self.test_num})
        self.UTILS.reporting.logComment("Using target telephone number " + self.cont["tel"]["value"])

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Clear it all
        #
        self.messages.deleteAllThreads()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()

        #
        # Insert the phone number in the To field
        #
        self.messages.addNumbersInToField([self.test_num])

        #
        # Create SMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()
        self.messages.waitForReceivedMsgInThisThread()
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Open contacts app and create a contact with the same phone number used to send the SMS in the
        # previous step
        #
        self.contacts.launch()
        self.contacts.createNewContact(self.cont)

        #
        # Switch back to the messages app.
        #
        # self.UTILS.app.switchToApp("Messages")
        self.messages.launch()

        #
        # Verify the thread now contains the name of the contact instead of the phone number
        #
        self.UTILS.reporting.logComment("Trying to open the thread with name: " + self.cont["name"])
        self.messages.openThread(self.cont["name"])
