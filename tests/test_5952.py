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

class test_5952(GaiaTestCase):
    _Description = "[SMS] CLONE - Try to send empty SMS."
    
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
        self.messages.addNumberInToField(self.target_telNum)

        #
        # Tap the message area.
        #
        x = self.UTILS.getElement(DOM.Messages.input_message_area, "Message body input field")
        x.tap()

        #
        # Check the 'Send button isn't enabled yet.
        #
        x = self.UTILS.getElement(DOM.Messages.send_message_button, "Send message button")
        self.UTILS.TEST(not x.is_enabled(), 
                        "Send button is not enabled after target number is supplied, but message still empty.")
        
