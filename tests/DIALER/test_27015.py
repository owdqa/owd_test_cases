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
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
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

        self.Contact_1 = MockContact()
        self.num  = "0034" + self.Contact_1["tel"]["value"]
        #self.num  = "0034" + self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.Contact_2 = MockContact()

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Create a call log.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()
 
        #
        # Open the call log and create a contact for our number.
        #
        self.dialer.callLog_createContact(self.num)
 
        contFields = self.contacts.get_contact_fields()
        self.contacts.replace_str(contFields['givenName'  ] , self.Contact_2["givenName"])
        self.contacts.replace_str(contFields['familyName' ] , self.Contact_2["familyName"])
 
        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()
 
        #
        # Verify that the contacts app is closed and we are returned to the call log.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements( ("xpath", "//iframe[contains(@%s, '%s')]" % \
                                                (DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                        "Contacts frame")
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)
 
        self.UTILS.element.waitForElements( ("xpath", "//h1[text()='Call log']"), "Call log header")

        #
        # Verify that this contact has been created in contacts.
        #
        self.apps.kill_all()
        self.contacts.launch()
        self.contacts.view_contact(self.Contact_2["name"])
