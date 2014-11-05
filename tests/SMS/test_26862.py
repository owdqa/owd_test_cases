#===============================================================================
# 26862: Try send a sms creating a new thread while airplane is enabled
#
# Pre-requisites:
# Enable flight mode
#
# Procedure:
# 1- Open sms app
# 2- Write a phone number (no contact number and there isn't thread for his number)
# 3- write a text and press send
# ER1
# 4- Pres OK
# ER2
#
# Expected results:
# ER1 A confirmation dialog should be shown to the user stating "in order to send
# a message you must first disable Flight Safe Mode" and an "OK" button.
# ER2 When the "OK" button is pressed, the dialogue is closed and the user is
# returned to the SMS thread view. The sms must be shown with an X icon on the right.
# The new SMS thread must be created.
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
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

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        #
        # Put the phone into airplane mode.
        #
        self.data_layer.set_setting('airplaneMode.enabled', True)
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.data_layer.set_setting('airplaneMode.enabled', False)
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        self.messages.launch()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()

        #
        # Insert the phone number in the To field
        #
        self.messages.addNumbersInToField([self.phone_number])

        #
        # Create SMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Click send.
        #
        self.messages.sendSMS()

        time.sleep(3)

        #
        # Check that popup appears.
        #
        self.messages.checkAirplaneModeWarning()

        # Check an error indication is shown in message
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        msg = self.messages.last_message_in_this_thread()
        indication = msg.get_attribute("class").index("error") != -1
        self.UTILS.test.test(indication == True, "An indication error was found")
