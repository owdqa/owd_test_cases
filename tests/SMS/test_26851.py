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


class test_main(GaiaTestCase):

    test_msg = "Test message."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.target_telNum = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.startNewSMS()

        #
        # Enter the number.
        #
        self.messages.addNumbersInToField([self.target_telNum])

        #
        # Enter the message.
        #
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Send the SMS.
        #
        sendBtn = self.UTILS.element.getElement(DOM.Messages.send_message_button, "Send sms button")
        sendBtn.tap()

        #
        # Lock the phone immediately.
        #
        self.lockscreen.lock()

        #
        # Wait for the notification.
        #
        self.UTILS.element.getElement(("xpath",
                        DOM.Messages.lockscreen_notif_xpath.format(self.target_telNum)),
                        "New message notification while screen is locked", False, 120, False)
