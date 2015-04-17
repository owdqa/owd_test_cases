#
# TC_MMSTC-FEATR-012d
# The device should support MPEG4 file format
from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.video import Video


class test_main(PixiTestCase):

    test_msg = "Hello World"

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.video = Video(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        self.messages.create_and_send_mms('video', [self.phone_number], self.test_msg)

        self.messages.wait_for_message()
        # Verify we have received an MMS
        self.messages.verify_mms_received('video', self.phone_number)
