# 28015: Add number with prefix as new contact
# ** Procedure
# 1. Dial a number with international prefix and press "add to contact" button
#       2. Select "Create new contact"
#       3. Add info contacts (name, last name, company, another phone number, email, address) and press "update" button
#       4. Close dialer and open contacts
# ** Expected Results
#       2. The "Edit contact" window is displayed
#       3. User is taken back to dialer
#       4. Verify that now you have one contact and all info have been saved correctly

import sys
sys.path.insert(1, "./")
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact
from tests.i18nsetup import setup_translations


class test_main(PixiTestCase):

    def setUp(self):
        # Set up child objects...
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)
        _ = setup_translations(self)

        self.contact_1 = MockContact()
        self.phone_number = "0034" + self.UTILS.general.get_config_variable("target_call_number", "common")

        # Generate an entry in the call log
        self.dialer.launch()
        self.dialer.callLog_clearAll()
        self.dialer.createMultipleCallLogEntries(self.phone_number, 1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):

        #
        # Open the call log and create a contact for our number.
        #
        self.dialer.callLog_createContact(self.phone_number)

        contFields = self.contacts.get_contact_fields()
        self.contacts.replace_str(contFields['givenName'], self.contact_1["givenName"])
        self.contacts.replace_str(contFields['familyName'], self.contact_1["familyName"])

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
        self.contacts.view_contact(self.contact_1["name"])
