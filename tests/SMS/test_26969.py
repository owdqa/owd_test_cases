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
        self.messages.waitForReceivedMsgInThisThread()
        
        self.tryTheLink(0, self._link1)
        self.tryTheLink(1, self._link2)
        self.tryTheLink(2, self._link3)

    def tryTheLink(self, p_linkNum, p_link):
        self.UTILS.logResult("info", "Tapping <b>%s</b> ..." % p_link)
        
        #
        # Switch to messaging app.
        #
        self.apps.kill_all()
        time.sleep(2)
        self.messages.launch()
        self.messages.openThread(self.target_telNum)

        #
        # Get last message.
        #
        x = self.messages.waitForReceivedMsgInThisThread()
 
        #
        # Find all URLs
        #
        y=x.find_elements("tag name", "a")
 
        #
        # Tap on required link.
        #
        y[p_linkNum].tap()
 
        #
        # Give the browser time to start up, then
        # switch to the browser frame and check the page loaded.
        #
        time.sleep(2)
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        
        self.UTILS.TEST(self.browser.check_page_loaded(p_link),
                 "Web page " + str(p_linkNum+1) + " loaded correctly.")