#===============================================================================
# 29895: Send a MMS when data is off and wifi on
#
# Pre-requisites:
# Commercial SIM needed for this test
#
# Procedure:
# 1. Open messaging app
# 2. Create a new MMS
# 3. Tap on send
#
# Expected results:
# The MMS is sent.
#===============================================================================

from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.settings import Settings


class test_main(PixiTestCase):

    # Restart device to start with wifi and 3g disabled.
    #
    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)
        self.settings = Settings(self)

        self.test_msg = "Hello World"

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Turn on wifi connection.
        #
        self.data_layer.connect_to_wifi()

        #
        # Create and Send an MMS
        #
        self.messages.create_and_send_mms("image", [self.phone_number], self.test_msg)
        #
        # Verify that the MMS has been received.
        #
        self.messages.wait_for_message()
        self.messages.verify_mms_received("img", self.phone_number)
