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
from OWDTestToolkit.apps import Contacts
from tests._mock_data.contacts import MockContact
import time


class test_main(GaiaTestCase):
    test_msg = "Test text - please ignore."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)
        
   
        #
        # Prepare the contact we're going to insert.
        #
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel = {'type': 'Mobile', 'value': self.num1})

        self.UTILS.insertContact(self.contact)

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
        self.contacts.viewContact(self.contact['name'])
         
        #
        # Tap the sms button in the view details screen to go to the sms page.
        #
        smsBTN = self.UTILS.getElement(DOM.Contacts.sms_button, "Send SMS button")
        smsBTN.tap()
 
        #
        # Switch to the 'Messages' app frame (or marionette will still be watching the
        # 'Contacts' app!).
        #
        time.sleep(5)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
 
        self.UTILS.headerCheck("1 recipient")     
        self.messages.checkIsInToField(self.contact['name'])
        
        # Not present in 'master' branch because of multiple target number fnuctionality.
#         #
#         #  Check the carrier is displayed here.
#         #
#         x = self.UTILS.getElement(DOM.Messages.type_and_carrier_field, "Contact phone 'type' and 'carrier' field")
#         
#         self.UTILS.TEST( self.contact_1["tel"]["type"]    in x.text, "Phone type is in the header.")
#         self.UTILS.TEST( self.contact_1["tel"]["carrier"] in x.text, "Phone carrier is in the header.")
