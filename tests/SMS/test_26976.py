#===============================================================================
# 26976: Click on an email address in a sms which contains 3 emails addresses
#
# Procedure:
# 1. Send a sms from "device A" to "device B" who contains 3 emails addresses
# 2. Open the thread view in the device A
# 3. Hold on the second email
# 4. Press create conctat button
#
# Expected results:
# Contact app is launched with the correct email in email address field
#===============================================================================

from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.emailAddy = self.UTILS.general.get_config_variable("gmail_1_email", "common")
        self.test_msg = "Email {} one, email {} two, email {} three.".\
                        format("one@test.com", self.emailAddy, "three@test.com")
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.create_and_send_sms([self.phone_number], self.test_msg)
        send_time = self.messages.last_sent_message_timestamp()
        msg = self.messages.wait_for_message(send_time=send_time)

        #
        # Long press the 2nd email link.
        #
        link = msg.find_elements(*DOM.Messages.email_info_in_msg)
        self.UTILS.element.simulateClick(link[1])

        #
        # Click 'create new contact'.
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_create_new_contact_btn, "Create new contact button")
        x.tap()

        #
        # Verify that the email is in the email field.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        x = self.UTILS.element.getElement(("id", "email_0"), "Email field")
        x_txt = x.get_attribute("value")
        self.UTILS.test.test(x_txt == self.emailAddy, "Email is '{}' (expected '{}')".format(x_txt, self.emailAddy))
