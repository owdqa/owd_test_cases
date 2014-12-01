#===============================================================================
# 26863: Try send a sms in an existing thread while airplane is enabled
#
# Procedure:
# 1- Open sms app
# 2- Write a phone number (no contact number and there is a thread for
# his number)
# 3- write a text and press send
# ER1
# 4- Press OK
# ER2
#
# Expected results:
# ER1 A confirmation dialog should be shown to the user stating "in order
# to send a message you must first disable Flight Safe Mode" and an "OK" button.
# ER2 When the "OK" button is pressed, the dialogue is closed and the user is
# returned to the SMS thread view.
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.target_num = self.UTILS.general.get_config_variable("GLOBAL_TARGET_SMS_NUM")
        self.test_msg = "Test."
        self.data_layer.delete_all_sms()

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
        self.messages.wait_for_message(send_time=send_time)

        self.UTILS.home.goHome()

        #
        # Put the phone into airplane mode.
        #
        self.UTILS.statusbar.toggleViaStatusBar('airplane')

        self.UTILS.reporting.debug("*** Launching messages again!!!")
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
