#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *


class test_main(GaiaTestCase):
    
    _TestMsg     = "Hello World"
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.gallery    = Gallery(self)
        self.actions    = Actions(self.marionette)
        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending mms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):

        #
        # Load an image file into the device.
        #
        self.UTILS.addFileToDevice('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()
        
        #
        # Insert the phone number in the To field
        #
        self.messages.addNumbersInToField([ self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM") ])

        #
        # Create MMS.
        #
        self.messages.enterSMSMsg(self._TestMsg)
        self.messages.createMMSImage()
        self.gallery.clickThumbMMS(0)


        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()

        #
        # This step is necessary because our sim cards receive mms with +XXX
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        self.messages.openThread("+" + self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))

        #
        # Wait for the last message in this thread to be a 'recieved' one.
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)


        #
        # Open mms option with longtap on it
        #
        self.UTILS.logResult("info", "Open mms option with longtap on it")
        x = self.UTILS.getElement(DOM.Messages.received_mms, "Target mms field")
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
        # Send the mms.
        #
        self.UTILS.logResult("info", "Cliking on Send button")
        x = self.UTILS.getElement(DOM.Messages.send_message_button, "Send button is displayed")
        x.tap()


        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()


        #
        # This step is necessary because our sim cards receive mms with +XXX
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        self.messages.openThread("+" + self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))

        #
        # Wait for the last message in this thread to be a 'recieved' one.
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)