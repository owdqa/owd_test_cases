#
# MMSTC-PREST-006a
# Multiple objects in same page

import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.music import Music


class test_main(SpreadtrumTestCase):

    test_msg = "Hello World"

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)
        self.music = Music(self)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)

        # Load files into the device.
        self.UTILS.general.add_file_to_device('./tests/_resources/80x60.jpg')
        self.UTILS.general.add_file_to_device('./tests/_resources/AMR.amr')

    def tearDown(self):
        self.UTILS.general.remove_files()
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.messages.launch()

        self.messages.startNewSMS()
        self.messages.addNumbersInToField([self.phone_number])
        self.messages.enterSMSMsg(self.test_msg)
        self.messages.create_mms_image()
        self.gallery.click_on_thumbnail_at_position_mms(0)

        time.sleep(2)
        self.messages.create_mms_music()
        self.music.click_on_song_mms()

        self.messages.sendSMS()
        self.messages.wait_for_message()
        self.messages.verify_mms_received("img", self.phone_number)
        self.messages.verify_mms_received("audio", self.phone_number)
