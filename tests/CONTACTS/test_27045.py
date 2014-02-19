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
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.settings   = Settings(self)

        self.gmail_u = self.UTILS.get_os_variable("GMAIL_1_USER")
        self.gmail_p = self.UTILS.get_os_variable("GMAIL_1_PASS")

        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContact()
        self.Contact_2 = MockContact(email = '')
        
        self.UTILS.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.UTILS.getNetworkConnection()
         
        self.contacts.launch()

        self.contacts.import_GmailLogin(self.gmail_u, self.gmail_p)

        x = self.UTILS.getElements(DOM.Contacts.import_conts_list, "Contact list", False)
         
        gmail_contacts = []
        for y in x:
            contNam = y.get_attribute("data-search")
            if '#search#' not in contNam:
                self.UTILS.logResult("info", "Adding '%s' to the list of available contacts." % contNam)
                gmail_contacts.append(contNam)
             
        self.contacts.import_ImportAll()

        self.apps.kill_all()

        self.contacts.launch()
        
        self.UTILS.logResult("info", "Viewing contact '%s' ..." % gmail_contacts[0]) 
        self.contacts.viewContact("roytesterton.1@hotmail.com", False)

        editBTN = self.UTILS.getElement(DOM.Contacts.edit_details_button, "Edit details button")
        editBTN.tap()
        self.UTILS.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contacts' screen header")

        #
        # Enter the new contact details.
        #
        contFields = self.contacts.getContactFields()
        self.contacts.replaceStr(contFields['givenName'  ] , self.Contact_2["givenName"])
        self.contacts.replaceStr(contFields['familyName' ] , self.Contact_2["familyName"])
        self.contacts.replaceStr(contFields['tel'        ] , self.Contact_2["tel"]["value"])
        self.contacts.replaceStr(contFields['street'     ] , self.Contact_2["adr"]["streetAddress"])
        self.contacts.replaceStr(contFields['zip'        ] , self.Contact_2["adr"]["postalCode"])
        self.contacts.replaceStr(contFields['city'       ] , self.Contact_2["adr"]["locality"])
        self.contacts.replaceStr(contFields['country'    ] , self.Contact_2["adr"]["countryName"])
        
        #
        # Save the changes
        #
        updateBTN = self.UTILS.getElement(DOM.Contacts.edit_update_button, "Edit 'update' button")
        updateBTN.tap()
        
        time.sleep(2)
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)


