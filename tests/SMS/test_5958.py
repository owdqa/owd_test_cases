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

class test_5958(GaiaTestCase):
    _Description = "[SMS] CLONE - Send a new SMS using the option of reduced list of favourite contacts."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.contacts   = Contacts(self)
        
        #
        # Import some contacts.
        #
        self.Contact_1 = MockContacts().Contact_1
        self.Contact_2 = MockContacts().Contact_2
        self.Contact_3 = MockContacts().Contact_longName
        self.Contact_4 = MockContacts().Contact_multiplePhones
        self.Contact_5 = MockContacts().Contact_multipleEmails

        # Set the one we'll match to have a valid phone number.
        self.Contact_1["tel"]["value"] = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Using target telephone number " + self.Contact_1["tel"]["value"])
        
        # Set a couple of them to be favorites (including the one we'll use).
        self.Contact_1["category"] = "favorite"
        self.Contact_2["category"] = "favorite"
        
        # Insert all the contacts.
        self.data_layer.insert_contact(self.Contact_1)
        self.data_layer.insert_contact(self.Contact_2)
        self.data_layer.insert_contact(self.Contact_3)
        self.data_layer.insert_contact(self.Contact_4)
        self.data_layer.insert_contact(self.Contact_5)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Type a message containing the required string 
        #
        self.messages.startNewSMS()
        self.messages.enterSMSMsg("Test message")
        
        #
        # Search for our contact in the favourites section.
        #
        orig_iframe = self.messages.selectAddContactButton()
        
        x = self.UTILS.getElement( ("xpath", DOM.Contacts.favourites_list_xpath % self.Contact_1['name'].replace(" ", "")),
                                   "'" + self.Contact_1['name'] + "' in the favourites section")
        x.tap()

        #
        # Switch back to the sms iframe.
        #
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame("src",orig_iframe)
        
        #
        # Now check the correct name is in the 'To' list.
        #
        self.messages.checkIsInToField(self.Contact_1["name"])
        self.messages.sendSMS()
        
        #
        # Receiving the message is not part of the test, so just wait a 
        # few seconds for the returned sms in case it messes up the next test.
        #
        time.sleep(5)
