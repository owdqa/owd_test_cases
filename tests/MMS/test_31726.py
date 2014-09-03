#===============================================================================
# 31726: 3GPP Video
#
# Procedure:
# The purpose is to verify that a QCIF video file/object is correctly
# sent from Client A (DuT) to Client B and that the QCIF video file/object
# is reasonably presented.
# 1. In Client A (DuT), create a new MM.
# 2. In MM header: To-field is set to Client B.
# 3. In MM content: Add video file/object qcif_video.3gp to the message.
# 4. In Client A (DuT), send MM to Client B.
# 5. In Client B, receive and open the MM.
# 6. Verify the pass criteria below.
#
# Expected results:
# Client B has received the message and the QCIF video file/object
# is reasonably presented and QCIF video file/object is played in its entirety.
# ADDITIONAL INFO:
# FOR CL:
# When played, the video must fit the size of the DUT screen, otherwise
# the test must be reported as fail."
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.video import Video


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.video = Video(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.target_mms_number = self.UTILS.general.get_os_variable("TARGET_MMS_NUM")
        self.test_msg = "Hello World"
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.general.remove_file('mpeg4.mp4', "SD/mus")
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()
        #
        # Load files into the device.
        self.UTILS.general.addFileToDevice('./tests/_resources/mpeg4.mp4', destination='SD/mus')

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()

        #
        # Insert the phone number in the To field
        #
        self.messages.addNumbersInToField([self.phone_number])

        #
        # Create MMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        self.messages.createMMSVideo()
        self.video.clickOnVideoMMS(0)

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()
        self.UTILS.statusbar.wait_for_notification_toaster_title(self.target_mms_number, timeout=120)
        self.UTILS.statusbar.click_on_notification_title(self.target_mms_number, timeout=30)
        self.messages.verifyMMSReceived("video", self.target_mms_number)
