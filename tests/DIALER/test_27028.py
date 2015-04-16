# 27028: Add to an existing contact from a number which is in the call log with several entries (All tab)
# ** Procedure
#       1. Open call log
#       2. Tap on Unknown number
#       3. Select "Add to an existing contact"
#       4. Select the a contact available
#       5. Press "update"
#       6. Close call log, open contacts and then open the contact
# ** Expected Results
#       1. Several entries with call to/from a number with unknown name is displayed
#       2. The "select from" menu is displayed
#       3. the "select contact" page is displayed;
#       4. The "edit contact" page is displayed
#       5. User is taken back to call log page
#       6. Contacts is updated with correct name and phone number

from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact


class test_main(FireCTestCase):

    def setUp(self):
        # Set up child objects...
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        self.target_call_number = self.UTILS.general.get_config_variable("target_call_number", "common")

        self.test_contact = MockContact()
        self.UTILS.general.insertContact(self.test_contact)

        # Generate an entry in the call log
        self.dialer.launch()
        self.dialer.callLog_clearAll()
        self.dialer.createMultipleCallLogEntries(self.target_call_number, 2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # Add to our contact.
        #
        self.dialer.callLog_addToContact(self.target_call_number, self.test_contact["name"])

        #
        # Verify that this contact has been modified in contacts.
        #
        self.contacts.launch()
        self.contacts.view_contact(self.test_contact["name"])

        self.UTILS.element.waitForElements(("xpath", DOM.Contacts.view_contact_tels_xpath.format(self.target_call_number)),
                                           "Telephone phone_numberber {} in contact".format(self.target_call_number))
