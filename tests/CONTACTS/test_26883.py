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

    _RESTART_DEVICE = True

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
        tlf =  self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.Contact_1 = MockContact(tel = {'type': 'Mobile', 'value': tlf})

        self.UTILS.logComment("Using target telephone number " + self.Contact_1["tel"]["value"])
        
        #
        # Add this contact (quick'n'dirty method - we're just testing sms, no adding a contact).
        #
        self.UTILS.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Make sure we have no threads (currently blocked - use _RESTART_DEVICE instead).
        #
#         self.messages.launch()
#         self.messages.deleteAllThreads()
#         self.UTILS.touchHomeButton()

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
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)

#         #
#         # TEST: this automatically opens the 'send SMS' screen, so
#         # check the correct name is in the header of this sms.
#         #
#         self.UTILS.TEST(self.UTILS.headerCheck(self.contact_1['name']),
#                         "'Send message' header = '" + self.contact_1['name'] + "'.")
    
        #
        # Create SMS.
        #
        x=self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "frame", x)
        self.messages.enterSMSMsg(self._TestMsg)
        
        #
        # Click send.
        #
        self.messages.sendSMS()
