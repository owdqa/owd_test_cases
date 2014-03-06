#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Messages

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
        
        bool7OK = False
        bool8OK = False
        bool9OK = False
        for i in y:
            self.UTILS.logResult("info", "FYI: %s is highlighted." % i.text)
            if i.text == "1234567":
                bool7OK = True
            if i.text == "12345678":
                bool8OK = True
            if i.text == "123456789":
                bool9OK = True
                
        self.UTILS.TEST(bool7OK, "The 8-digit number is highlighted.")
        self.UTILS.TEST(bool8OK, "The 8-digit number is highlighted.")
        self.UTILS.TEST(bool9OK, "The 9-digit number is highlighted.")

        