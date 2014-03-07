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
import time



class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)
        
        self.num  = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.Contact_1 = MockContact()
                
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.dialer.launch()
        
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()

        self.dialer.callLog_createContact(self.num)
        
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
         
        self.UTILS.waitForElements( ("xpath", "//h1[text()='Call log']"), "Call log header")
        
        #
        # Verify that the call log now shows the contact name,
        #
        x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % self.num),
                                   "The call log for number %s" % self.num)

        self.UTILS.TEST(self.Contact_1["name"] in x.text, "Call log now shows '%s'." % self.Contact_1["name"])