#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")

from gaiatest   import GaiaTestCase
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

        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Start by making sure we have no other notifications.
        #
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message (don't use api - I want to be back in homepage
        # before the sms has finshed sending and the api waits).
        #
        newMsgBtn = self.UTILS.element.getElement(DOM.Messages.create_new_message_btn,
                                        "Create new message button")
        newMsgBtn.tap()

        self.messages.addNumbersInToField([self.target_telNum])
        self.messages.enterSMSMsg(self.test_msg)

        self.marionette.execute_script("document.getElementById('" + \
                                             DOM.Messages.send_message_button[1] + \
                                             "').click();")

        #
        # Bit of a race: QUICKLY go 'home' and wait for the notifier.
        # If we're not quick enough the returned sms will arrive while we're still in
        # messaging, in which case the statusbar notifier will never appear.
        #
        self.UTILS.home.goHome()
        self.messages.waitForSMSNotifier(self.target_telNum)

        #
        # Click the notifier.
        #
        self.messages.clickSMSNotifier(self.target_telNum)

        #
        # TEST: The returned message is as expected (caseless in case user typed it manually).
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        sms_text = returnedSMS.text
        self.UTILS.test.TEST((sms_text.lower() == self.test_msg.lower()),
            "SMS text = '" + self.test_msg + "' (it was '" + sms_text + "').")

        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Check the message via the thread.
        #
        self.messages.openThread(self.target_telNum)

        #
        # TEST: The returned message is as expected (caseless in case user typed it manually).
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        sms_text = returnedSMS.text
        self.UTILS.test.TEST((sms_text.lower() == self.test_msg.lower()), 
            "SMS text = '" + self.test_msg + "' (it was '" + sms_text + "').")

