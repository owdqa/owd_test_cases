#===============================================================================
# 29923: Verify that the user can receive attached a file .mp3 in a MMS and
# it is displayed as audio
#
# Procedure:
# 1 Send a mms with a file .mp3 attached to a test device
# ER1
# 2. Open the received MMS in the test device
# 3. Open the file received attached in the mms
# ER2
#
# Expected result:
# ER1 The MMS is received in the test device
# ER2 The MMS and the attached filed can be opened.
#===============================================================================

import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.music import Music
from OWDTestToolkit import DOM


class test_main(FireCTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.music = Music(self)

        self.test_msg = "Hello World"

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.music.tap_play()
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        # Create and Send an MMS with a audio attached.
        self.messages.create_and_send_mms("audio", [self.phone_number], self.test_msg)

        self.messages.wait_for_message()
        self.messages.verify_mms_received("audio", self.phone_number)
        self.messages.open_attached_file(DOM.Music.frame_locator)
        time.sleep(5)
        self.music.is_player_playing()
