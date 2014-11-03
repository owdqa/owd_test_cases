#===============================================================================
# 31730: Reception of video file + JPG file + AMR file
#
# Pre-requisites:
# DuT with properly configured MM settings. Another reference handset to send MM.
#
# Procedure:
# 1. With a reference handset, create a new MM.
# 2. In MM header: To-field is set to DuT.
# 3. MM content: In the message object part, enter a 3GPP video file, JPG image
# and AMR file.
# 4. With the reference handset, send MM to DUT.
# 5. In DuT receive and open the MM.
# 6. Verify the MM (with all previous contents described) is properly shown.
#
# Expected results:
# The MM shall be correctly received by the DUT.
#===============================================================================

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.music import Music
from OWDTestToolkit.apps.video import Video


class test_main(GaiaTestCase):

    test_msg = "Hello World {}".format(time.time())

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)
        self.music = Music(self)
        self.video = Video(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()
        self.expected_sizes = ["4.8", "62.3", "175.6"]
        self.expected_names = ["80x60.jpg", "30k_basic_AMR.amr", "mpeg4.3gp"]

        self.UTILS.general.addFileToDevice('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')
        self.UTILS.general.addFileToDevice('./tests/_resources/30k_basic_AMR.amr', destination='SD/mus')
        self.UTILS.general.addFileToDevice('./tests/_resources/mpeg4.mp4', destination='SD/vid')

    def tearDown(self):
        self.UTILS.general.remove_file('30k_basic_AMR.amr', '/SD/mus')
        self.UTILS.general.remove_file('mpeg4.mp4', '/SD/vid')
        self.UTILS.general.remove_file('80x60.jpg', 'DCIM/100MZLLA')
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        self.messages.launch()

        self.messages.startNewSMS()
        self.messages.addNumbersInToField([self.phone_number])
        self.messages.enterSMSMsg(self.test_msg)

        self.messages.createMMSImage()
        self.gallery.click_on_thumbnail_at_position_mms(0)

        self.messages.createMMSMusic()
        self.music.click_on_song_mms()

        self.messages.createMMSVideo()
        self.video.click_on_video_at_position_mms(0)

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()
        last_msg = self.messages.wait_for_message()
        attachments = self.messages.get_mms_attachments_info(last_msg)
        self.UTILS.reporting.debug("*** ATTACHMENTS: {}".format(attachments))

        # Check the names and sizes of all attachments are as expected
        for (i, att) in enumerate(attachments):
            self.UTILS.test.TEST(self.expected_names[i] == att["name"] and self.expected_sizes[i] == att["size"],
                                 "Attachment [{}] ({}kb)     Expected [{}] ({}kb)".\
                                 format(self.expected_names[i], self.expected_sizes[i],
                                        att["name"], att["size"]))
