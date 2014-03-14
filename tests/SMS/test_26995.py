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
from OWDTestToolkit.apps.messages import Messages

class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
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
        test_str = "Four 1234 six 123456 seven 1234567 eight 12345678 nine 123456789 numbers."
        self.messages.createAndSendSMS([self.num1], test_str)
        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Check how many are links.
        #
        fnam = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot (for reference):", fnam)

        y = x.find_elements("tag name", "a")  
                
        bool4OK = True
        bool6OK = True
        for i in y:
            self.UTILS.logResult("info", "FYI: {} is highlighted.".format(i.text))
            if i.text == "1234":
                bool4OK = False
            if i.text == "123456":
                bool7OK = False
                
        self.UTILS.TEST(bool4OK, "The 4-digit number is not highlighted.")
        self.UTILS.TEST(bool6OK, "The 6-digit number is not highlighted.")

        