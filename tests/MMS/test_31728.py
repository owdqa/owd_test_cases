#
# 31728 - Receiving MP4 audio file

from gaiatest import GaiaTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.music import Music


class test_main(GaiaTestCase):

    test_msg = "Hello World"

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.music = Music(self)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.messages.create_and_send_mms('audio', [self.phone_number], self.test_msg)
        self.messages.wait_for_message()
        self.messages.verify_mms_received('audio', self.phone_number)
