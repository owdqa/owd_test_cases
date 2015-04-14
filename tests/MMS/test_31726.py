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

from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.video import Video


class test_main(FireCTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.video = Video(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.test_msg = "Hello World"
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.general.remove_file('mpeg4.mp4', "SD/mus")
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()
        self.messages.create_and_send_mms('video', [self.phone_number], self.test_msg)
        self.messages.verify_mms_received("video", self.phone_number)
