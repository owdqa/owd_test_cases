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
    
    _link        = "www.google.com"
    _TestMsg     = "Test " + _link + " this."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.browser    = Browser(self)
        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending sms to telephone number " + self.target_telNum)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.UTILS.getNetworkConnection()
        
        #
        # Launch messages app.
        #
        self.messages.launch()
          
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.target_telNum], self._TestMsg)
          
        #
        # Wait for the last message in this thread to be a 'received' one
        # and click the link.
        #
        x = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(x, "Received a message.", True)
        
        #
        # Go into message edit mode and tap on edit button.
        #
        y= self.UTILS.getElement(DOM.Messages.edit_messages_icon, "Edit button" )
        y.tap()
       
        x.find_element("tag name", "a").tap()
       
        z=self.UTILS.getElement(DOM.Messages.edit_msgs_header,"1 selected message")
        self.UTILS.TEST(z.text=="1 selected", "Into edit mode, if you tap on link, the browser is not open and the message is selected.")
        
        
              
        