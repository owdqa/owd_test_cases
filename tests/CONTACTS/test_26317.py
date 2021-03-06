from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.email import Email
from OWDTestToolkit.utils.contacts import MockContact
import time


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.email = Email(self)

        # Get details of our test contacts.
        email1 = self.UTILS.general.get_config_variable("gmail_1_email", "common")
        email2 = self.UTILS.general.get_config_variable("gmail_2_email", "common")
        email3 = self.UTILS.general.get_config_variable("hotmail_1_email", "common")
        self.contact = MockContact(email=[{
            'type': 'Personal',
            'value': email1}, {
            'type': 'Personal',
            'value': email2}, {
            'type': 'Personal',
            'value': email3}
        ])
        """
        We're not testing adding a contact, so just stick one
        into the database.
        """

        self.UTILS.general.insertContact(self.contact)

        self._email_subject = "test " + str(time.time())
        self._email_message = "Test message"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        self.connect_to_network()

        # Set up to use email (with account #1).
        em_user = self.UTILS.general.get_config_variable("gmail_1_user", "common")
        em_email = self.UTILS.general.get_config_variable("gmail_1_email", "common")
        em_pass = self.UTILS.general.get_config_variable("gmail_1_pass", "common")
        self.email.launch()
        self.email.setup_account(em_user, em_email, em_pass)

        # Launch contacts app.
        self.contacts.launch()

        # View the details of our contact.
        self.contacts.view_contact(self.contact['name'])

        # Click the 2nd email button
        email_btn = self.UTILS.element.getElement(("id", DOM.Contacts.email_button_spec_id.format(1)),
                                        "2nd send Email address in for this contact")
        email_btn.tap()

        # Switch to email frame.
        time.sleep(1)
        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)

        # Verify the 'to' field is correct.
        expected_to = self.contact["email"][1]["value"]
        y = self.UTILS.element.getElement(DOM.Email.compose_to_from_contacts, "'To' field")
        self.UTILS.test.test(y.text == expected_to,
                        "The 'to' field contains '" + expected_to + "' (it was (" + y.text + ").")

        # Fill in the rest and send it.
        self.UTILS.general.typeThis(DOM.Email.compose_subject, "'Subject' field", self._email_subject, True, False)
        self.UTILS.general.typeThis(DOM.Email.compose_msg, "Message field", self._email_message, True, False, False)

        # Send the message.
        self.email.send_the_email_and_switch_frame(self.contact['name'], DOM.Contacts.frame_locator)
