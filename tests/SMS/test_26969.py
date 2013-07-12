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
    
    _link1        = "www.google.com"
    _link2        = "www.hotmail.com"
    _link3        = "www.wikipedia.org"
    _TestMsg     = "Test " + _link1 +" "+ _link2 +" "+_link3 + " this."
    
    
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
        # Find all URLs
        #
        y=x.find_elements("tag name", "a")
        
        #
        # Tap on first link
        #
        y[0].tap()
                   
        #
        # Give the browser time to start up, then
        # switch to the browser frame and check the page loaded.
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        
        self.UTILS.TEST(self.browser.check_page_loaded(self._link1),
                        "Web page 1 loaded correctly.")
        
        #
        # Go to Homescreen
        #
        time.sleep(3)
        self.UTILS.touchHomeButton()
        
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Go to the thread and received SMS.
        #
        self.messages.openThread(self.target_telNum)
        x = self.messages.waitForReceivedMsgInThisThread()
        y=x.find_elements("tag name", "a")
        
        #
        # Tap on second link
        #       
        y[1].tap()
        
        #
        # Give the browser time to start up, then
        # switch to the browser frame and check the page loaded.
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        
        self.UTILS.TEST(self.browser.check_page_loaded(self._link2),
                        "Web page 2 loaded correctly.")
        
        #
        # Go to Homescreen
        #
        time.sleep(3)
        self.UTILS.touchHomeButton()
        
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Go to the thread and received SMS.
        #
        self.messages.openThread(self.target_telNum)
        x = self.messages.waitForReceivedMsgInThisThread()
        y=x.find_elements("tag name", "a")
        
        #
        # Tap on third link
        #       
        y[2].tap()
        
        #
        # Give the browser time to start up, then
        # switch to the browser frame and check the page loaded.
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        
        self.UTILS.TEST(self.browser.check_page_loaded(self._link3),
                        "Web page 3 loaded correctly.")