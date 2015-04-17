from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.email import Email
from OWDTestToolkit.utils.contacts import MockContact
#import time


class test_main(PixiTestCase):

    test_msg = "Test message."

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.Email = Email(self)

        self.email_user = self.UTILS.general.get_config_variable("gmail_1_user", "common")
        self.email_address = self.UTILS.general.get_config_variable("gmail_1_email", "common")
        self.email_pass = self.UTILS.general.get_config_variable("gmail_1_pass", "common")
 
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.emailAddy = self.UTILS.general.get_config_variable("gmail_2_email", "common")

        self.contact = MockContact(email = {'type': 'Personal', 'value': self.emailAddy})

        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Set up email account.
        #
        self.connect_to_network()

        self.Email.launch()
        self.Email.setupAccount(self.email_user, self.email_address, self.email_pass)
 
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.create_and_send_sms([self.phone_number], "Email {} one.".format(self.emailAddy))
        x = self.messages.wait_for_message()

        #
        # Tap the email link.
        #
        link = x.find_element("tag name", "a")
        link.tap()

        #
        # Press 'add to existing contact' button.
        #
        w = self.UTILS.element.getElement(DOM.Messages.header_send_email_btn, "Send email button")
        w.tap()

        #
        # Switch to email frame and verify the email address is in the To field.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)
        x = self.UTILS.element.getElement(DOM.Email.compose_to_from_contacts, "To field")
        self.UTILS.test.test(x.text == self.emailAddy, 
                        "To field contains '{}' (it was '{}').".format(self.emailAddy, self.emailAddy))