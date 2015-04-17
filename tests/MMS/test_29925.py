#===============================================================================
# 29925: Verify that can attach a picture from the camera source
#
# Procedure:
# 1. Open Messaging app
# 2. Create a new message
# 3. Tap on the attach icon
# 4. Select Camera
# 5. Take a picture
# 6. Tap on Select
#
# Expected result:
# The picture taken is correctly attached to the MMS
#===============================================================================

from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)

        self.test_msg = "Hello World"

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Create and Send an MMS with a image attached.
        #
        self.messages.create_and_send_mms("cameraImage", [self.phone_number], self.test_msg)
        self.messages.wait_for_message()
        self.messages.verify_mms_received("img", self.phone_number)
