# 27030: Verify the call log is updated after 'Adding to an existing contact'
#
# ** Procedure
#       1. Open call log
#       2. Tap on Unknown number on an entry of the current day
#       3. Select "Add to an existing contact" (gmail, hotmail, facebook, manually saved, SIM)
#       4. Select the a contact available
#       5. Press "update"
#       6. Close call log, open it again
# ** Expected Result
#       1. Several entries with calls to/from a number with unknown name is displayed
#       2. The "select from" menu is displayed
#       3. the "select contact" page is displayed;
#       4. The "edit contact" page is displayed
#       5. User is taken back to call log page
#       6. Call log shows the contact's name just saved
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

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.test_contact = MockContact()
        self.UTILS.general.insertContact(self.test_contact)

        self.dialer.launch()
        self.dialer.callLog_clearAll()
        self.dialer.createMultipleCallLogEntries(self.phone_number, 1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.callLog_addToContact(self.phone_number, self.test_contact["name"])

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

        #
        # Re-open the call log and Verify that it now shows the contact name,
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@{}, '{}')]".
                                               format(DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                              "Contacts frame")

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)
        header = ('xpath', DOM.GLOBAL.app_head_specific.format(_("Call log")))
        self.UTILS.element.waitForElements(header, "Call log header")

        x = self.UTILS.element.getElement(("xpath", DOM.Dialer.call_log_number_xpath.format(self.phone_number)),
                                          "The call log for number {}".format(self.phone_number))

        self.UTILS.test.test(
            self.test_contact["name"] in x.text, "Call log now shows '{}'".format(self.test_contact["name"]))
