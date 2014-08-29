# 27027: Create a contact from a number which is in the call log with several entries (All tab)
# ** Procedure
#       1. Open call log
#       2. Tap on an Unknown number
#       3. Select "Create new contact"
#       4. Add name of the contact and press "update"
#       5. Close call log, open contacts and then open the new contact
# ** Expected Results
#       1. Several entries with call to a number with unknown name is displayed
#       2. The "select from" menu is displayed
#       3. The "edit contact" page is displayed
#       4. User is taken back to call log page
#       5. contacts now has one entry; the new contact has correct name and phone number

import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact
from tests.i18nsetup import setup_translations


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)
        _ = setup_translations(self)

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.test_contact = MockContact()

        # Generate an entry in the call log
        self.dialer.launch()
        self.dialer.callLog_clearAll()
        self.dialer.createMultipleCallLogEntries(self.phone_number, 2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        self.dialer.callLog_createContact(self.phone_number)

        contFields = self.contacts.get_contact_fields()
        self.contacts.replace_str(contFields['givenName'], self.test_contact["givenName"])
        self.contacts.replace_str(contFields['familyName'], self.test_contact["familyName"])

        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()

        #
        # Verify that the contacts app is closed and we are returned to the call log.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@{}, '{}')]".\
                                               format(DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                              "Contacts frame")
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

        header = ('xpath', DOM.GLOBAL.app_head_specific.format(_("Call log")))
        self.UTILS.element.waitForElements(header, "Call log header")

        #
        # Verify that this contact has been created in contacts.
        #
        self.apps.kill_all()
        time.sleep(2)
        self.contacts.launch()
        self.contacts.view_contact(self.test_contact["name"])
