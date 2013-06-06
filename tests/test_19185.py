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

class test_19185(GaiaTestCase):
    _Description = "[CONTACTS] The 'done' button in new contact mode (email parameter)."
    
    _email_addy = "one_two@myemail.com"

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
                
        #
        #

        #
        # Launch contacts app.
        #
        self.contacts.launch()

        
    
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Click create new contact.
        #
        self.contacts.startCreateNewContact()
        
        #
        # Verify that the 'DONE' button is disabled just now.
        #
        done_button = self.UTILS.getElement(DOM.Contacts.done_button, "'Done' button")
        self.UTILS.TEST(done_button.is_enabled() == False, "Done button is disabled by default.")
        
        #
        # Add some info. to the email field.
        #
        self.UTILS.typeThis(DOM.Contacts.email_field, "Email field", self._email_addy)
        
        #
        # Verify that the 'DONE' button is enabled just now.
        #
        done_button = self.UTILS.getElement(DOM.Contacts.done_button, "'Done' button")
        self.UTILS.TEST(done_button.is_enabled() == True, "Done button is enabled if email is filled in.")

        #
        # Press the DONE button and return to the view all contacts screen.
        #        
        done_button.tap()
        self.UTILS.waitForElements(DOM.Contacts.view_all_header, "View all contacts header")

        #
        # Verify that our contact is now present with the email address as his
        # contact name.
        #
        x = ("xpath", DOM.Contacts.view_all_contact_name_xpath % self._email_addy)
        self.UTILS.waitForElements(x, "Contact '" + self._email_addy + "'")
