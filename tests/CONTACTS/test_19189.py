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
from tests._mock_data.contacts import MockContacts
import time

class test_19189(GaiaTestCase):
    _Description = "[CONTACTS] Add multiple emails addresses."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        
        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContacts().Contact_1
        self.data_layer.insert_contact(self.Contact_1)
        
        
    
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # View the contact details.
        #
        self.contacts.viewContact(self.Contact_1['name'])
        
        #
        # Edit the contact.
        #
        self.contacts.pressEditContactButton()
        
        #
        # Count the current email addresses.
        #
        orig_count = self.contacts.countEmailAddressesWhileEditing()
        
        #
        # Add a few email addresses.
        #
        self.contacts.addAnotherEmailAddress("one@myemail.com")
        self.contacts.addAnotherEmailAddress("two@myemail.com")
        
        #
        # Get the new count.
        #
        new_count = self.contacts.countEmailAddressesWhileEditing()
        
        #
        # Verify there are 3 more.
        #
        diff = (new_count - orig_count)
        self.UTILS.TEST( diff == 2,
                        "3 more emails listed for this contact before saving the changes (there were " + str(diff) + ") .")
        
        #
        # Save the changes.
        #
        x = self.UTILS.getElement(DOM.Contacts.edit_update_button, "Update button")
        x.tap()
        
        #
        # Back to 'view all' screen.
        #
        x = self.UTILS.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()
        
        #
        # View the contact again.
        #
        self.contacts.viewContact(self.Contact_1['name'])
        
        #
        # Count the email fields.
        #
        x = self.UTILS.getElements(DOM.Contacts.email_address_list, "Email addresses", False)
        view_count=0
        email1_found=False
        email2_found=False
        email3_found=False
        for i in x:
            if "email-details-template-" in i.get_attribute("id"):
                view_count = view_count + 1
                btn_name = i.find_element("tag name", "button").text
                
                self.UTILS.logResult("info", "    - " + btn_name)
                if btn_name == "one@myemail.com":
                    email1_found = True
                if btn_name == "two@myemail.com":
                    email2_found = True
                
        self.UTILS.TEST(view_count == new_count, str(new_count) + " emails are displayed.")
        
        self.UTILS.TEST(email1_found, "First added email is present.")        
        self.UTILS.TEST(email2_found, "Second added email is present.")       
        
    
