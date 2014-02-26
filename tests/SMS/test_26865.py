#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *
import time

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):
    
    _TestMsg     = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.messages   = Messages(self)

        #
        # Prepare the contact we're going to insert.
        #
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.Contact_1 = MockContact(givenName = 'AAAAAAAAAAAAAAAALEX', familyName = 'SMITHXXXXXXXX',
                                     name = 'AAAAAAAAAAAAAAAALEX SMITHXXXXXXXX',
                                     tel = {'type': 'Mobile', 'value': self.num1})

        self.UTILS.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.messages.launch()

        self.messages.createAndSendSMS( [self.Contact_1["tel"]["value"]],
                                        "(Just bypassing bug 867119!)")
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # View the details of our contact.
        #
        self.contacts.viewContact(self.Contact_1['name'])
        
        #
        # Tap the sms button in the view details screen to go to the sms page.
        #
        smsBTN = self.UTILS.getElement(DOM.Contacts.sms_button, "Send SMS button")
        smsBTN.tap()

        #
        # Switch to the 'Messages' app frame (or marionette will still be watching the
        # 'Contacts' app!).
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)

        #
        # Create SMS.
        #
        self.messages.enterSMSMsg(self._TestMsg)
        
        #
        # Click send.
        #
        self.messages.sendSMS()
        
        #
        # Wait for the last message in this thread to be a 'recieved' one.
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)
        
        #
        # TEST: The returned message is as expected (caseless in case user typed it manually).
        #
        sms_text = returnedSMS.text
        self.UTILS.TEST((sms_text.lower() == self._TestMsg.lower()), 
            "SMS text = '" + self._TestMsg + "' (it was '" + sms_text + "').")