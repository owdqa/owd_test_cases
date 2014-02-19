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
import time
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):
    
    _link        = "owdqatestone@gmail.com"
    _TestMsg     = "Test " + _link + " this."
    
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.contacts   = Contacts(self)
        
        #
        # Insert a contact without email addresses
        # 
        self.UTILS.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')        
        self.Contact_1 = MockContact(email = {'type': 'Personal', 'value': ''})

        self.UTILS.insertContact(self.Contact_1)
   
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending sms to telephone number " + self.target_telNum)
        
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
        self.messages.createAndSendSMS([self.target_telNum], self._TestMsg)
          
        #
        # Wait for the last message in this thread to be a 'received' one
        # and click the link.
        #
        x = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(x, "Received a message.", True)
        
        a=x.find_element("tag name", "a")
        
        a.tap()
        
        #
        # Press 'add to existing contact' button.
        #
        w = self.UTILS.getElement(DOM.Messages.header_add_to_contact_btn, "Add to existing contact button")
        w.tap()
                
        #
        # Switch to Contacts app.
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
        #
        # Select the contact.
        #
        z = self.UTILS.getElement(DOM.Contacts.view_all_contact_JS, "Search item")
        z.tap()   
         
        #
        # Fill out all the other details.
        #
        contFields = self.contacts.getContactFields()
        
        #
        # Put the contact details into each of the fields (this method
        # clears each field first).
        #
        self.contacts.replaceStr(contFields['givenName'  ] , self.Contact_1["givenName"]+"bis")
        self.contacts.replaceStr(contFields['familyName' ] , self.Contact_1["familyName"]+"bis")
        self.contacts.replaceStr(contFields['tel'        ] , self.Contact_1["tel"]["value"]+"bis")
        self.contacts.replaceStr(contFields['street'     ] , self.Contact_1["adr"]["streetAddress"]+"bis")
        self.contacts.replaceStr(contFields['zip'        ] , self.Contact_1["adr"]["postalCode"]+"bis")
        self.contacts.replaceStr(contFields['city'       ] , self.Contact_1["adr"]["locality"]+"bis")
        self.contacts.replaceStr(contFields['country'    ] , self.Contact_1["adr"]["countryName"]+"bis")
        self.contacts.addGalleryImageToContact(0)
                
        #
        # Add another email address.
        #
        self.contacts.addAnotherEmailAddress(self.Contact_1["email"]["value"])
        
        #
        # Press the Done button.
        #
        done_button = self.UTILS.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()

        #
        # Check that the contacts iframe is now gone.
        #
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@src,'contacts')]"),
                                       "Contact app iframe")
        
        #
        # Now return to the SMS app.
        #
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)