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
import time

class test_19180(GaiaTestCase):
    _Description = "(BLOCKED BY BUG 879823) [FACEBOOK] Unlink all Facebook contacts in the address book in a single step and verify the contacts who was linked to a facebook contacts."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.facebook   = Facebook(self)
                
        #
        #

        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContacts().Contact_1
        self.data_layer.insert_contact(self.Contact_1)
    
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):        
        self.UTILS.getNetworkConnection()
        
        #
        # Launch contacts app and enable facebook import.
        #
        self.contacts.launch()

        self.contacts.tapSettingsButton()
        
        self.contacts.enableFBImport()        
        fb_user = self.UTILS.get_os_variable("T19180_FB_USERNAME")
        fb_pass = self.UTILS.get_os_variable("T19180_FB_PASSWORD")
        self.facebook.login(fb_user, fb_pass)
        
        #
        # Import facebook contacts.
        #
        self.contacts.switchToFacebook()
        friend_count = self.facebook.importAll()

        #
        # View the contact details.
        #
        self.contacts.launch()
        self.contacts.viewContact(self.Contact_1['name'])
         
        #
        # Press the link button.
        #
        self.contacts.tapLinkContact()
 
        #
        # Select the contact to link.
        #
        fb_email = self.UTILS.get_os_variable("T19180_FB_LINK_EMAIL_ADDRESS")

        self.facebook.LinkContact(fb_email)
         
        #
        # Check we're back at our contact.
        #
        self.UTILS.headerCheck(self.Contact_1['name'])
 
        #
        # Verify that we're now linked.
        #
        self.contacts.verifyLinked(self.Contact_1['name'], fb_email)



