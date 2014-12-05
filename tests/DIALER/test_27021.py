# 27021: Add call log entry to existing contact (with more phone numbers) and contacts not empty
# ** Procedure
#       1. Open call log
#       2. Tap on Unknown number
#       3. Select "Add to an existing contact"
#       4. Select the only contact available
#       5. Press "update"
#       6. Close call log, open contacts and then open the contact
# ** Expected Results
#       1. An entry with call to a number with unknown name is displayed
#       2. The "select from" menu is displayed
#       3. the "select contact" page is displayed; it has a single contact
#       4. The "edit contact" page is displayed
#       5. User is taken back to call log page
#       6. Contacts has one entry; verify that the contact is correct and previous phone numbers
#          have not been overwritten by the new one
#
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.phone_number2 = self.UTILS.general.get_config_variable("short_phone_number", "custom")

        self.test_contact = MockContact(tel={'type': 'Mobile', 'value': self.phone_number2})
        self.UTILS.general.insertContact(self.test_contact)

        # Generate an entry in the call log
        self.dialer.launch()
        self.dialer.callLog_clearAll()
        self.dialer.createMultipleCallLogEntries(self.phone_number, 1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Open the call log and add to our contact.
        #
        self.dialer.callLog_addToContact(self.phone_number, self.test_contact["name"])

        #
        # Verify that this contact has been modified in contacts.
        #
        self.contacts.launch()
        self.contacts.view_contact(self.test_contact["name"])

        self.UTILS.element.waitForElements(("xpath", DOM.Contacts.view_contact_tels_xpath.format(self.phone_number)),
                                           "Telephone number {} in contact".format(self.phone_number))
