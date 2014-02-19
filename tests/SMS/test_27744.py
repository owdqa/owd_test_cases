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
        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending sms to telephone number " + self.target_telNum)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Start a new sms.
        #
        self.messages.startNewSMS()
        
        #
        # Enter a number in the target field.
        #
        self.messages.addNumbersInToField([self.target_telNum])

        #
        # Enter a message the message area.
        #
        x = self.messages.enterSMSMsg("xxx")
        
        #
        # Click the back button.
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        
        #
        # Check for the 'discard confirmation' popup.
        #

        self.marionette.switch_to_frame()
        x = self.UTILS.getElement( ("xpath", "//*[text()='Are you sure you want to discard this message?']"),
                                   "Discard confirmation message", True, 5, False)
        x = self.UTILS.getElement(DOM.GLOBAL.modal_confirm_ok2, "OK button", True, 5, False)
        x.tap()

        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        
        #
        # Verify that we're now in the correct place.
        #
        self.UTILS.headerCheck("Messages")
