#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)

        self.actions    = Actions(self.marionette)

        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending sms to telephone number " + self.target_telNum)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Sometimes causes a problem if not cleared.
        #
        self.UTILS.clearAllStatusBarNotifs()

        #
        # Create message - 5 x 10 chars.
        #
        sms_message = ""
        for i in range(0,5):
            sms_message = sms_message + "0123456789"
            
        sms_message_length = len(sms_message)
        self.UTILS.logComment("Message length sent: " + str(sms_message_length))
        
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.target_telNum], sms_message)
        
        #
        # Wait for the last message in this thread to be a 'recieved' one.
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)

        #
        # Back to send a new sms
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Create and send a new test message. Repeat this steps to having several sms in the thread
        #
        self.messages.createAndSendSMS([self.target_telNum], sms_message)

        #
        # Wait for the last message in this thread to be a 'recieved' one.
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)

        #
        # Open sms option with longtap on it
        #
        self.UTILS.logResult("info", "Open sms option with longtap on it")
        x = self.UTILS.getElement(DOM.Messages.received_sms, "Target sms field")
        self.actions.long_press(x, 2).perform()

        #
        # Press fordward button
        #
        self.UTILS.logResult("info", "Cliking on fordaward button")
        x = self.UTILS.getElement(DOM.Messages.fordward_btn_msg_opt, "Fordward button is displayed")
        x.tap()

        #
        # Add a phone number.
        #
        self.messages.addNumbersInToField([self.target_telNum])

        #
        # Send the sms.
        #
        self.UTILS.logResult("info", "Cliking on Send button")
        x = self.UTILS.getElement(DOM.Messages.send_message_button, "Send button is displayed")
        x.tap()


        #
        # Wait for the last message in this thread to be a 'recieved' one.
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)

