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

class test_main(GaiaTestCase):

    test_msg = "This text has multiple spaces 1 2 3 4 5."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Remove number and import contact.
        #
        self.telNum = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.telNum)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Send a message containing the required string 
        #
        self.messages.startNewSMS()
        self.messages.addNumbersInToField([self.telNum])
        self.messages.enterSMSMsg(self.test_msg)
        self.messages.sendSMS()

        #
        # Check the receievd message.
        #
        x = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.test.TEST(x.text == self.test_msg, 
                        "The text in the message received matches the message that was sent." +\
                        "|EXPECTED: '" + self.test_msg + "'" + \
                        "|ACTUAL  : '" + x.text + "'")
