# 27016: Add short number to an existing contact with different number
# ** Procedure
#       1. Dial a short (only few digits) phone number and press "add to contact" button
#       2. Select "Add to an existing contact"
#       3. Select the contact available
#       4. Press "update" button
#       5. Close dialer and open contacts
# 
# ** Expected Results
#       2. The "Select contact" window is opened
#       3. The "Edit contact" window is opened
#       4. User is taken back to dialer
#       5. Verify that existing contact has been updated with the new phone number
import time
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact


class test_main(PixiTestCase):

    def setUp(self):
        # Set up child objects...
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.phone_number_short = self.UTILS.general.get_config_variable("short_phone_number", "custom")

        # Remove the phone number from the contact and insert it.
        self.test_contact = MockContact(tel={'type': 'Mobile', 'value': self.phone_number})
        self.UTILS.general.insertContact(self.test_contact)

         # Generate an entry in the call log
        self.dialer.launch()
        self.dialer.callLog_clearAll()
        self.dialer.createMultipleCallLogEntries(self.phone_number_short, 1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Open the call log and add to our contact.
        #
        self.dialer.callLog_addToContact(self.phone_number_short, self.test_contact["name"])

        #
        # Verify that this number was added to the contact.
        #
        self.apps.kill_all()
        time.sleep(2)
    
        self.contacts.launch()
        self.contacts.view_contact(self.test_contact["name"])

        self.UTILS.element.waitForElements(("xpath", DOM.Contacts.view_contact_tels_xpath.format(self.phone_number_short)),
                                    "New phone number {} in this contact".format(self.phone_number_short))
