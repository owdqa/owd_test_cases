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
<<<<<<< HEAD
from tests._mock_data.contacts import MockContacts
=======
>>>>>>> 40c7f2a67c7a723ed348afb42e134ae039d6199d

class test_main(GaiaTestCase):
    
    _TestMsg     = "Test message."
    
<<<<<<< HEAD
    
=======
>>>>>>> 40c7f2a67c7a723ed348afb42e134ae039d6199d
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
<<<<<<< HEAD
        self.contacts   = Contacts(self)
        
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.emailAddy = self.UTILS.get_os_variable("GMAIL_1_EMAIL")
=======
        self.Email      = Email(self)

        self.USER1  = self.UTILS.get_os_variable("GMAIL_1_USER")
        self.EMAIL1 = self.UTILS.get_os_variable("GMAIL_1_EMAIL")
        self.PASS1  = self.UTILS.get_os_variable("GMAIL_1_PASS")
         
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.emailAddy = self.UTILS.get_os_variable("GMAIL_2_EMAIL")
        
>>>>>>> 40c7f2a67c7a723ed348afb42e134ae039d6199d
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
<<<<<<< HEAD
=======
        
        #
        # Set up email account.
        #
        self.UTILS.getNetworkConnection()        
        self.Email.launch()
        self.Email.setupAccount(self.USER1, self.EMAIL1, self.PASS1)
 
>>>>>>> 40c7f2a67c7a723ed348afb42e134ae039d6199d
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Create and send a new test message.
        #
<<<<<<< HEAD
        self.messages.createAndSendSMS([self.num1], "Hello " + self.emailAddy + " old bean.")
        x=self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Tap on edit mode.
        #
        y=self.UTILS.getElement(DOM.Messages.edit_messages_icon, "Edit button")
        y.tap()  
         
        #
        # Long press the email link.
        #    
        _link = x.find_element("tag name", "a")
        self.actions    = Actions(self.marionette)
        self.actions.long_press(_link,2).perform() 
        
        #
        # Check the email address is not a link in edit mode.
        #
        self.UTILS.waitForNotElements( ("xpath", "//button[text()='Create new contact']"),
                                   "Create new contact button")
=======
        self.messages.createAndSendSMS([self.num1], "Email addy %s test." % self.emailAddy)
        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Go into edit mode.
        #
        self.UTILS.logResult("info", "Go into edit mode.")
        x = self.UTILS.getElement(DOM.Messages.edit_messages_icon, "Edit button")
        x.tap()
        
        #
        # Tap the email link.
        #
        x = self.messages.lastMessageInThisThread()
        self.UTILS.logResult("info", "Tap the email address in this message: '%s'." % x.text)
        _link = x.find_element("tag name", "a")
        _link.tap()
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Messaging app screenshot after tapping link:", x)
        
        #
        # The email application should not be launched.
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@src,'email')]"),
                                       "Email app iframe", True, 5, False)
        
        try:
            x = self.marionette.find_element("xpath", "//iframe[contains(@src,'email')]")
            self.marionette.switch_to_frame(x)
            x = self.UTILS.screenShotOnErr()
            self.UTILS.logResult("info", "<b>Screenshot of email app:</b> ", x)
        except:
            pass
>>>>>>> 40c7f2a67c7a723ed348afb42e134ae039d6199d
