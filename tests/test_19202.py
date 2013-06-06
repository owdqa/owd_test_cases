#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#

class test_19202(GaiaTestCase):
    _Description = "(BLOCKED BY BUG 879816) [SMS] Delete a sms conversation."
    
    _TestMsg1 = "First message."
    _TestMsg2 = "Second message"
    _TestMsg3 = "Third message"
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = AppMessages(self)
         
         
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
        # Create and send some new tests messages.
        #
        self.messages.createAndSendSMS([self.target_telNum], self._TestMsg1)
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Go back..
        #
        x= self.UTILS.getElement(DOM.Messages.header_back_button, "Back button" )
        x.tap()
        
        #
        # Delete this thread.
        #
        self.messages.deleteThreads([self.target_telNum])
                
        #
        # Check thread isn't there anymore.
        #
        self.UTILS.waitForNotElements(("xpath", DOM.Messages.thread_selector_xpath % self.target_telNum),"Thread") 
                
