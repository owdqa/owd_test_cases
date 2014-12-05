#===============================================================================
# 26977: Verify that when in edit mode, adding email contact from sms is disabled
#
# Procedure:
# 1. Send a sms from "device A" to "device B" which contains an email address
# 2. Open sms app in the device A.
# 3. Tap on edit icon
# 4. Tap on the email in the sms view
#
# Expected results:
# Nothing should happen as in edit mode this functionality is disabled
#===============================================================================

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from marionette import Actions


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.contacts = Contacts(self)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.emailAddy = self.UTILS.general.get_config_variable("gmail_1_email", "common")
        self.test_msg = "Hello {} old bean at {}.".format(self.emailAddy, time.time())

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
        self.messages.create_and_send_sms([self.phone_number], self.test_msg)
        send_time = self.messages.last_sent_message_timestamp()
        msg = self.messages.wait_for_message(send_time=send_time)
        self.messages.check_last_message_contents(self.test_msg)

        #
        # Tap on edit mode.
        #
        edit_btn = self.UTILS.element.getElement(DOM.Messages.edit_messages_icon, "Edit button")
        edit_btn.tap()

        #
        # Verify that the Delete Messages button is present and press it to enter in Edit mode
        #
        delete_btn = self.UTILS.element.getElement(DOM.Messages.delete_threads_button, "Delete threads button present")
        delete_btn.tap()

        #
        # Long press the email link.
        #
        _link = msg.find_element("tag name", "a")
        self.actions = Actions(self.marionette)
        self.actions.long_press(_link, 2).perform()

        #
        # Check the email address is not a link in edit mode.
        #
        self.UTILS.element.waitForNotElements(DOM.Messages.header_create_new_contact_btn, "Create new contact button")
