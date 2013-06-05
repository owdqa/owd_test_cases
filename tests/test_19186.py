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

class test_19186(GaiaTestCase):
    _Description = "[CONTACTS] Delete all characters to the name and surname fields."
    
    _testName    = "Obi"
    _testSurname = "Wan"

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = AppContacts(self)
                
        #
        #
    
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Click create new contact.
        #
        self.contacts.startCreateNewContact()
        
        
        #####################################True
        #
        # Given name ...
        #
        
        #
        # Add some info. to the field.
        #
        self.UTILS.typeThis(DOM.Contacts.given_name_field, 
                            "Given name field", 
                            self._testName,
                            p_no_keyboard=False, 
                            p_clear=True, 
                            p_enter=False, 
                            p_validate=True,
                            p_remove_keyboard=False)
        
        #
        # Press the 'x'.
        #
        x = self.UTILS.getElement(DOM.Contacts.given_name_reset_icon, "Given name reset icon")
        x.tap()

        #
        # Click the header, then verify that the field contains nothing.
        #
        self.marionette.find_element("tag name", "h1").tap()
        x = self.UTILS.getElement(DOM.Contacts.given_name_field, "Given name field")
        self.UTILS.TEST(x.text == "", "Given name field is empty after being cleared.")
        
                
        #####################################
        #
        # Surname ...
        #
        
        #
        # Add some info. to the field.
        #
        self.UTILS.typeThis(DOM.Contacts.family_name_field, 
                            "Surname field", 
                            self._testSurname,
                            p_no_keyboard=False, 
                            p_clear=True, 
                            p_enter=False, 
                            p_validate=True,
                            p_remove_keyboard=False)
        
        #
        # Press the 'x'.
        #
        x = self.UTILS.getElement(DOM.Contacts.family_name_reset_icon, "Surname reset icon")
        x.tap()

        #
        # Click the header, then verify that the field contains nothing.
        #
        self.marionette.find_element("tag name", "h1").tap()
        x = self.UTILS.getElement(DOM.Contacts.family_name_field, "Surname field")
        self.UTILS.TEST(x.text == "", "Surname field is empty after being cleared.")
                
