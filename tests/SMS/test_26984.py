#===============================================================================
# 26984: Verify that the action menu with the different options given to user
# is shown correctly
#
# Pre-requisites:
# Receive an SMS from a number which is not stored on the Address book
#
# Procedure:
# 1. Open the SMS
# 2. On the thread view tap on the header where the number is shown
#
# Expected results:
# The user should be prompted about the action he would like to perform:
# Call, Create a new contact, Add to an existing contact and Cancel.
# Besides the number appears on top of these acctions
#===============================================================================

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.target_number = self.UTILS.general.get_config_variable("target_call_number", "common")
        self.test_msg = "Test message."
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()

        # Create and send a new test message.
        expected = "Test {} number.".format(self.target_number)
        self.messages.create_and_send_sms([self.phone_number], expected)
        send_time = self.messages.last_sent_message_timestamp()
        self.messages.wait_for_message(send_time=send_time)
        self.messages.check_last_message_contents(expected)

        # Tap the header.
        x = self.UTILS.element.getElement(DOM.Messages.message_header, "Thread header")
        x.tap()

        # Verify that each expected item is present.
        self.UTILS.element.waitForElements(DOM.Messages.header_call_btn, "Call button")
        self.UTILS.element.waitForElements(DOM.Messages.header_create_new_contact_btn,
                                    "Create new contact button")
        self.UTILS.element.waitForElements(DOM.Messages.header_add_to_contact_btn,
                                    "Add to existing contact button")
        self.UTILS.element.waitForElements(DOM.Messages.contact_cancel_btn,
                                    "Cancel button")
        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult('info', "Screenshot", screenshot)
