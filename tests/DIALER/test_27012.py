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
from OWDTestToolkit.apps import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact



class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)
        
        self.Contact_1 = MockContact()
        self.num  = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Enter a number in the dialer.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        
        #
        # Press the add to contacts button, then select 'add to existing contact'.
        #
        x = self.UTILS.getElement(DOM.Dialer.add_to_contacts_button, "Add to contacts button")
        x.tap()
        
        x = self.UTILS.getElement(DOM.Dialer.create_new_contact_btn, "Create new contact button")
        x.tap()

        #
        # Enter the details of the new contact.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        contFields = self.contacts.getContactFields()
        self.contacts.replaceStr(contFields['givenName'  ] , self.Contact_1["givenName"])
        self.contacts.replaceStr(contFields['familyName' ] , self.Contact_1["familyName"])
         
        done_button = self.UTILS.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()
 
        #
        # Verify that the contacts app is closed and we are returned to the call log.
        #
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@%s, '%s')]" % \
                                                (DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                        "COntacts frame")
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)
         
        #
        # Verify that this contact has been created in contacts.
        #
        self.apps.kill_all()
        self.contacts.launch()
        self.contacts.viewContact(self.Contact_1["name"])
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Final screenshot and html dump:", x)        