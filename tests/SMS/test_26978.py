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
from OWDTestToolkit.apps.email import Email
import time

class test_main(GaiaTestCase):
    
    test_msg = "Test message."
    _RESTART_DEVICE = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.Email = Email(self)

        self.USER1 = self.UTILS.get_os_variable("GMAIL_1_USER")
        self.EMAIL1 = self.UTILS.get_os_variable("GMAIL_1_EMAIL")
        self.PASS1 = self.UTILS.get_os_variable("GMAIL_1_PASS")
         
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.emailAddy = self.UTILS.get_os_variable("GMAIL_2_EMAIL")
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Set up email account.
        #
        self.UTILS.getNetworkConnection()
 
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.num1], "Email address {} test.".format(self.emailAddy))
        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Tap the 2nd email link.
        #
        self.UTILS.logResult("info", "Click the email address in this message: '%s'." % x.text)
        _link = x.find_element("tag name", "a")
        _link.tap()

        #
        # Tap on "Send email" button from the overlay
        #
        x = self.UTILS.getElement(DOM.Messages.header_send_email_btn, "Send email button")
        x.tap()


        time.sleep(4)
        self.marionette.switch_to_frame()

        #
        # Confirm we want to setUp our email account
        #
        x = self.UTILS.getElement(DOM.Email.confirm_ok, "Set up account confirmation")
        x.tap()
        
        self.UTILS.switchToFrame(*DOM.Email.frame_locator)
        self.Email.setupAccount(self.USER1, self.EMAIL1, self.PASS1)
        
        #
        # Verify the email address is in the To field.
        #
        x = self.UTILS.getElement(DOM.Email.compose_to_from_contacts, "To field")
        self.UTILS.TEST(x.text == self.emailAddy, 
                        "To field contains '{0}' (it was '{0}').".format(self.emailAddy))
        
        #
        # Fill in the details and send the email.
        #
        self.UTILS.typeThis(DOM.Email.compose_subject, "'Subject' field", "Test email", True, False)
        self.UTILS.typeThis(DOM.Email.compose_msg, "Message field"  , "Just a test", True, False, False)

        self.Email.sendTheMessage()