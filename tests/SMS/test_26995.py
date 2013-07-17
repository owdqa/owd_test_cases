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
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Create and send a new test message.
        #
        test_str = "Four 1234 seven 1234567 eight 12345678 nine 123456789 numbers."
        self.messages.createAndSendSMS([self.num1], test_str)
        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Check how many are links.
        #
        fnam = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot (for reference):", fnam)

        y = x.find_elements("tag name", "a")  
                
        bool4OK = True
        bool7OK = True
        for i in y:
            self.UTILS.logResult("info", "FYI: %s is highlighted." % i.text)
            if i.text == "1234":
                bool4OK = False
            if i.text == "1234567":
                bool7OK = False
                
        self.UTILS.TEST(bool4OK, "The 4-digit number is not highlighted.")
        self.UTILS.TEST(bool7OK, "The 7-digit number is not highlighted.")

        