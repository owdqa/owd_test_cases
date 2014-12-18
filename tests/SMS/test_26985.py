from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages

class test_main(GaiaTestCase):

    test_msg = "Test message."

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.num1 = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.num2 = "621234567"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()

        # Create and send a new test message.
        self.messages.create_and_send_sms([self.num1], "Test {} number.".format(self.num2))
        x = self.messages.wait_for_message()

        # Enter edit mode.
        x = self.UTILS.element.getElement(DOM.Messages.edit_messages_icon, "Edit button")
        x.tap()

        # Tap the edit header.
        self.UTILS.reporting.logResult("info", "<b>NOTE:</b> This is the original number header, but really should be threads-edit-mode (marionette might be corrected for this, so switch the code to that if it starts failing)")
        x = self.UTILS.element.getElement(DOM.Messages.message_header, "Thread header (edit header)")
        x.tap()

        # Verify that nothing happened.
        self.UTILS.element.waitForNotElements(DOM.Messages.header_call_btn,
                                        "Call button")
        self.UTILS.element.waitForNotElements(DOM.Messages.header_create_new_contact_btn,
                                        "Create new contact button")
        self.UTILS.element.waitForNotElements(DOM.Messages.header_add_to_contact_btn,
                                        "Add to existing contact button")
        self.UTILS.element.waitForNotElements(DOM.Messages.contact_cancel_btn,
                                        "Cancel button")





        