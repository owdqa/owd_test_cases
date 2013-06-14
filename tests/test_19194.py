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
from tests.mock_data.contacts import MockContacts

class test_19194(GaiaTestCase):
    _Description = "[SMS] Try send a sms to a contact while airplane is enabled (from sms app - use contact option)."
    
    _TestMsg     = "Test."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.contacts   = Contacts(self)
        
        
        #
        # Prepare the contact we're going to insert.
        #
        self.contact_1 = MockContacts().Contact_1

        #
        # Establish which phone number to use.
        #
        self.contact_1["tel"]["value"] = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Using target telephone number " + self.contact_1["tel"]["value"])
        
        #
        # Add this contact (quick'n'dirty method - we're just testing sms, no adding a contact).
        #
        self.data_layer.insert_contact(self.contact_1)
        
        #
        # Put the phone into airplane mode.
        #
        self.data_layer.set_setting('ril.radio.disabled', True)

        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch contacts app.
        #
        self.contacts.launch()
          
        #
        # View the details of our contact.
        #
        self.contacts.viewContact(self.contact_1['name'])
          
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
        # TEST: this automatically opens the 'send SMS' screen, so
        # check the correct name is in the header of this sms.
        #
        self.UTILS.headerCheck("1 recipient")
        self.messages.checkIsInToField(self.contact_1['name'])
      
        #
        # Create SMS.
        #
        self.messages.enterSMSMsg(self._TestMsg)
          
        #
        # Click send.
        #
        self.messages.sendSMS()


        #
        # Check that popup appears.
        #
        self.messages.checkAirplaneModeWarning()
               
        #
        # Check that this last message is marked as failed.
        #
        x = self.messages.lastMessageInThisThread()
        self.UTILS.TEST( "error" in x.get_attribute("class"),
                         "The last message in this thread is marked as 'error'.")
        
        
