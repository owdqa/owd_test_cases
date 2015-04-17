#===============================================================================
# 29900: MMS received with auto retrieve and when roaming enabled (data and wifi
#       connection available)
#
# Pre-requisites:
# Data connection and wifi enabled, phone is in home network
#
# Procedure:
# 1. Open settings -> Message settings
# 2. Select "On with roaming"
# 3. Tap on OK
# 4. Send an MMS to that phone
#
# Expected results:
# 1. Open message settings
# 2. Roamin option is enabled
# 3. Back to Message settings
# 4. The MMS is received ok
#===============================================================================

from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.settings import Settings


class test_main(PixiTestCase):

    # Restart device to starting with wifi and 3g disabled.
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
        self.UTILS.general.connect_to_cell_data()
        self.data_layer.connect_to_wifi()

        #
        # Configure Auto Retrieve as "on_with_r = On with roaming option" from messaging settings
        #
        self.settings.configure_mms_auto_retrieve("on_with_r")

        self.messages.create_and_send_mms("image", [self.phone_number], self.test_msg)
        self.messages.wait_for_message()
        #
        # Verify that the MMS has been received.
        #
        self.messages.verify_mms_received("img", self.phone_number)
