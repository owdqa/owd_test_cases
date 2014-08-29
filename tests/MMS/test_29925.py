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

from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)

        self.test_msg = "Hello World"

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.mms_sender = self.UTILS.general.get_os_variable("TARGET_MMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Create and Send an MMS with a image attached.
        #
        self.messages.createAndSendMMS("cameraImage", [self.phone_number], self.test_msg)
        #
        # Verify that the MMS has been received.
        #
        self.UTILS.statusbar.wait_for_notification_toaster_title(self.mms_sender, timeout=120)
        self.messages.verifyMMSReceived("img", self.mms_sender)
