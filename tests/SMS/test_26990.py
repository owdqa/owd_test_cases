from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages

class test_main(GaiaTestCase):

    test_msg = "Test message."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.phone_number = self.UTILS.general.get_config_variable("short_phone_number", "custom")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.create_and_send_sms([self.phone_number], "Test message")

        #
        # The returned message won't come to this thread, so just tap the header.
        #
        x = self.UTILS.element.getElement(DOM.Messages.message_header,
                                    "Thread header (edit header)")
        x.tap()

        #
        # Verify that the options appear.
        #
        self.UTILS.element.waitForElements(DOM.Messages.header_call_btn,
                                    "Call button")
        self.UTILS.element.waitForElements(DOM.Messages.header_create_new_contact_btn,
                                    "Create new contact button")
        self.UTILS.element.waitForElements(DOM.Messages.header_add_to_contact_btn,
                                    "Add to existing contact button")
        self.UTILS.element.waitForElements(DOM.Messages.contact_cancel_btn,
                                    "Cancel button")




        