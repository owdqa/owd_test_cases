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
import time


class test_main(GaiaTestCase):

    test_msg = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.target_num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        self.UTILS.statusbar.toggleViaStatusBar('airplane')

    def test_run(self):
        #
        # Create a new SMS
        #
        self.messages.launch()
        self.messages.startNewSMS()

        #
        # Insert the phone number in the To field
        #
        self.messages.addNumbersInToField([self.target_num])

        #
        # Create SMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Click send.
        #
        self.messages.sendSMS()
        send_time = self.messages.last_sent_message_timestamp()

        #
        # Wait for the SMS to arrive.
        #
        self.messages.waitForReceivedMsgInThisThread(send_time=send_time)

        time.sleep(5)
        self.UTILS.home.goHome()

        #
        # Put the phone into airplane mode.
        #
        self.UTILS.statusbar.toggleViaStatusBar('airplane')

        self.messages.launch()
        #
        # Open sms app and go to the previous thread
        #
        self.messages.openThread(self.target_num)

        #
        # Create another SMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Click send.
        #
        self.messages.sendSMS()

        #
        # Check that popup appears.
        #
        self.messages.checkAirplaneModeWarning()
