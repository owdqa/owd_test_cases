# 27029: Verify the call log is updated after 'Creating a new contact'
#
# ** Procedure
#       1. Open call log
#       2. Tap on Unknown phone_numberber on an entry of the current day
#       3. Select "Create a new contact"
#       4. Write a name and press "update"
#       5. Close call log, open it again
#
# ** Expected Result
#       1. Several entries with calls to/from a phone_numberber with unknown name is displayed
#       2. The "select from" menu is displayed
#       3. The "edit contact" page is displayed
#       4. User is taken back to call log page
#       5. Call log shows the contact's name just saved

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

        self.dialer.launch()
        self.dialer.callLog_clearAll()
        self.dialer.createMultipleCallLogEntries(self.phone_number, 1)

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
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@{}, '{}')]".
                                               format(DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                              "Contacts frame")
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

        header = ('xpath', DOM.GLOBAL.app_head_specific.format(_("Call log")))
        self.UTILS.element.waitForElements(header, "Call log header")

        #
        # Verify that the call log now shows the contact name,
        #
        x = self.UTILS.element.getElement(("xpath", DOM.Dialer.call_log_number_xpath.format(self.phone_number)),
                                          "The call log for phone_number {}".format(self.phone_number))

        self.UTILS.test.TEST(self.test_contact["name"] in x.text, "Call log now shows '{}'.".
                             format(self.test_contact["name"]))
