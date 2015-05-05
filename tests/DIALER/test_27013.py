# OWD-27013: Add dialed number to existing contact without phone numbers 
# ** Procedure
#        1. Dial the number and press "add to contact" button
#        2. Select "Add to an existing contact"
#        3. Select the only contact available
#        4. Press "update" to save contact informations
#        5. Close dialer and open contacts
# ** Expected Results
#        2. Verify that it opens the "Select contact" window and it has only one entry
#        3. Verify that it opens the "Edit contact" window and the dialed phone number is added to contact numbers
#        4. User is taken back to the dialer
#        5. Verify that the contact has been correctly saved
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def setUp(self):
        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")

        # Remove the phone number from the contact and insert it.
        self.test_contact = MockContact(tel={'type': '', 'value': ''})
        self.UTILS.general.insertContact(self.test_contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Add a number and add it to an existing contact.
        self.dialer.launch()
        self.dialer.enterNumber(self.phone_number)
        self.dialer.addThisNumberToContact(self.test_contact["name"])

        self.UTILS.test.test(self.apps.displayed_app.name == self.dialer.app_name, "After adding number to contact we are taken back to Dialer")

        # Verify that this contact has been modified in contacts.
        self.apps.kill_all()
        self.contacts.launch()
        self.contacts.view_contact(self.test_contact["name"])

        contact_phone_number = self.UTILS.element.getElement(DOM.Contacts.view_contact_tel_field, "Contact telephone number")
        self.UTILS.test.test(self.phone_number in contact_phone_number.text, "Contact correctly updated with new phone number")
