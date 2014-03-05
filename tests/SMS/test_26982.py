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
from OWDTestToolkit.apps import Email

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
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.num1], "Email one one@tester.com, two %s , three three@tester.com." % self.emailAddy)
        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Tap the 2nd email link.
        #
        self.UTILS.logResult("info", "Click the 2nd email address in this message: '%s'." % x.text)
        _link = x.find_elements("tag name", "a")[1]
        _link.tap()
        
        #
        # Switch to email frame and verify the email address is in the To field.
        #
        self.UTILS.switchToFrame(*DOM.Email.frame_locator)
        x = self.UTILS.getElement(DOM.Email.compose_to_from_contacts, "To field")
        self.UTILS.TEST(x.text == self.emailAddy, 
                        "To field contains '%s' (it was '%s')." %
                        (self.emailAddy, self.emailAddy))