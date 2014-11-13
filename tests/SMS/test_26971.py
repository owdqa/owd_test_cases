#===============================================================================
# 26971: Verify that in the sms thread view, valid e-mail addresses will
# be highlighted or shown with a special visual indication
#
# Procedure:
# 1. Send a sms from "device A" to "device B" who contains an email address
# 2. Send a sms from "device B" to "device A" who contains an email address
# 3. Open the thread view in the device A
#
# Expected results:
# The email addresses will be highlighted or shown with a special visual
# indication
#===============================================================================

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.browser import Browser


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.browser = Browser(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.incoming_number = self.UTILS.general.get_os_variable("GLOBAL_CP_NUMBER").split(',')
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.emails = ["email1@test.com", "email2@test.com"]
        self.test_msg = "Test with email addresses: {} and {} at {}".format(self.emails[0], self.emails[1],
                                                                            time.time())
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.connect_to_network()

        self.messages.launch()

        self.messages.create_and_send_sms([self.phone_number], self.test_msg)
        send_time = self.messages.last_sent_message_timestamp()
        msg = self.messages.wait_for_message(send_time=send_time)

        #
        #Verify that a valid URL appears highlight on message received.
        #
        email_elems = msg.find_elements("tag name", "a")
        emails = [email.text for email in email_elems]
        all_found = all([email in emails for email in self.emails])
        self.UTILS.test.test(all_found, "All emails were found in the message")
