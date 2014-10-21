# 27020: Add call log entry to new contact
# ** Procedure
#       1. Open call log
#       2. Tap on an Unknown number
#       3. Select "Create new contact"
#       4. Add name of the contact and press "update"
#       5. Close call log, open contacts and then open new contact
# ** Expected Results
#       1. An entry with call to a number with unknown name is displayed
#       2. The "select from" menu is displayed
#       3. The "edit contact" page is displayed
#       4. User is taken back to call log page
#       5. contacts now has one entry; the new contact has correct name and phone number
#
import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact
from tests.i18nsetup import setup_translations

class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)
        _ = setup_translations(self)

        self.test_contact = MockContact()

        self.dialer.launch()
        self.dialer.callLog_clearAll()

        #
        # Create a call log entry
        #
        self.dialer.createMultipleCallLogEntries(self.test_contact["tel"]["value"], 2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Open the call log and create a contact for our number.
        #
        self.dialer.callLog_createContact(self.test_contact["tel"]["value"])

        contFields = self.contacts.get_contact_fields()
        self.contacts.replace_str(contFields['givenName'], self.test_contact["givenName"])
        self.contacts.replace_str(contFields['familyName'], self.test_contact["familyName"])

        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()

        #
        # Verify that the contacts app is closed and we are returned to the call log.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@{}, '{}')]".
                                               format(DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                              "Contacts frame")
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

        header = ('xpath', DOM.GLOBAL.app_head_specific.format(_("Call log")))
        self.UTILS.element.waitForElements(header, "Call log header")

        #
        # Verify that this contact has been created in contacts.
        #
        self.apps.kill_all()
        self.contacts.launch()
        self.contacts.view_contact(self.test_contact["name"])
