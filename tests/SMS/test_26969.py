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
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.browser import Browser
import time


class test_main(GaiaTestCase):
    
    links = ["www.google.com", "www.hotmail.com", "www.wikipedia.org"]
    test_msg = "Test " + " ".join(links) + " this."
    
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.browser = Browser(self)
        
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
        self.messages.createAndSendSMS([self.target_telNum], self.test_msg)
        self.messages.waitForReceivedMsgInThisThread()
        
        map(self.tryTheLink, range(len(self.links)), self.links)
        

    def tryTheLink(self, link_number, link):
        self.UTILS.logResult("info", "Tapping <b>{}</b> ...".format(link))
        
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
        y = x.find_elements("tag name", "a")
 
        #
        # Tap on required link.
        #
        y[link_number].tap()
 
        #
        # Give the browser time to start up, then
        # switch to the browser frame and check the page loaded.
        #
        time.sleep(2)
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        
        self.UTILS.TEST(self.browser.check_page_loaded(link),
                 "Web page {} loaded correctly.".format(link_number + 1))