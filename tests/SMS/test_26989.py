from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        prefix = "+34" if not phone_number.startswith("+34") else ""
        self.num1 = prefix + phone_number

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message to this contact.
        #
        self.messages.create_and_send_sms([self.num1], "Test message")
        self.messages.wait_for_message()

        #
        # Tap the header.
        #
        x = self.UTILS.element.getElement(DOM.Messages.message_header, "Thread header")
        x.tap()

        #
        # Verify that each expected item is present.
        #
        self.UTILS.element.waitForElements(DOM.Messages.header_call_btn,
                                    "Call button")
        self.UTILS.element.waitForElements(DOM.Messages.header_create_new_contact_btn,
                                    "Create new contact button")
        self.UTILS.element.waitForElements(DOM.Messages.header_add_to_contact_btn,
                                    "Add to existing contact button")
        self.UTILS.element.waitForElements(DOM.Messages.contact_cancel_btn,
                                    "Cancel button")
