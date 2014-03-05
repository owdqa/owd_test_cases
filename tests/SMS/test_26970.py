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
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Messages
from OWDTestToolkit.apps.browser import Browser
import time


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
        
        # Go into messages Settings..
        #
        z= self.UTILS.getElement(DOM.Messages.edit_messages_icon, "Edit button")
        z.tap()

        #
        # Go into message edit mode..
        #
        z= self.UTILS.getElement(DOM.Messages.delete_messages_btn, "Edit button")
        z.tap()
       
        y = x.find_element("tag name", "a")
        y.tap()
       
        z=self.UTILS.getElement(DOM.Messages.edit_msgs_header,"1 selected message")
        self.UTILS.TEST(z.text=="1 selected", "Into edit mode, if you tap on link, the browser is not open and the message is selected.")
        
        
        self.marionette.switch_to_frame()
        time.sleep(5) #(give the browser time to launch)
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@src,'browser')]"), "Browser iframe")