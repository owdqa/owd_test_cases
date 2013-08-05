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
    
    _TestMsg     = "Test message."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.Email      = Email(self)

        self.USER1  = self.UTILS.get_os_variable("GMAIL_1_USER")
        self.EMAIL1 = self.UTILS.get_os_variable("GMAIL_1_EMAIL")
        self.PASS1  = self.UTILS.get_os_variable("GMAIL_1_PASS")
         
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.emailAddy = self.UTILS.get_os_variable("GMAIL_2_EMAIL")
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Set up email account.
        #
        self.UTILS.getNetworkConnection()        
        self.Email.launch()
        self.Email.setupAccount(self.USER1, self.EMAIL1, self.PASS1)
 
        #
        # Disable the network connection.
        #
        self.UTILS.disableAllNetworkSettings()
 
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.num1], "Email addy %s test." % self.emailAddy)
        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Tap the 2nd email link.
        #
        self.UTILS.logResult("info", "Click the email address in this message: '%s'." % x.text)
        _link = x.find_element("tag name", "a")
        _link.tap()
        
        #
        # The email application should not be launched.
        #
        self.UTILS.logResult("info", "<b>When you know what the 'no network' warning looks like, replace this test with that one.</b>")
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@src,'email')]"),
                                       "Email app iframe", True, 5, False)
        
        try:
            elNam = ("xpath", "//iframe[contains(@src,'email')]")
            self.wait_for_element_present(*elNam, timeout=2)
            x = self.marionette.find_element(*elNam)
            self.marionette.switch_to_frame(x)
            x = self.UTILS.screenShotOnErr()
            self.UTILS.logResult("info", "<b>Screenshot of email app:</b> ", x)
        except:
            pass
