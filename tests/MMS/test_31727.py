#
# TC_MMSTC-FEATR-002c
# Sending PNG file
#
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery


class test_main(GaiaTestCase):

    test_msg = "Hello World"

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.messages.create_and_send_mms('image', [self.phone_number], self.test_msg)
        self.messages.wait_for_message()
        text = self.UTILS.element.getElement(DOM.Messages.last_message_mms_text, "Message text").text
        self.UTILS.test.test(text == self.test_msg, "[{}] received. Expected [{}]".format(text, self.test_msg), True)
        self.messages.verify_mms_received('img', self.phone_number)
