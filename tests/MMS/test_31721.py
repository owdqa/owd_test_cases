#
# MMSTC-PREST-006a
# Multiple objects in same page

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.music import Music


class test_main(GaiaTestCase):

    test_msg = "Hello World"

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)
        self.music = Music(self)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.target_mms_number = self.UTILS.general.get_os_variable("TARGET_MMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)

        # Load files into the device.
        self.UTILS.general.addFileToDevice('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')
        self.UTILS.general.addFileToDevice('./tests/_resources/AMR.amr', destination='SD/mus')

    def tearDown(self):
        self.UTILS.general.remove_file('80x60.jpg', 'DCIM/100MZLLA')
        self.UTILS.general.remove_file('AMR.amr', 'DCIM/100MZLLA')

        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.messages.launch()

        self.messages.startNewSMS()
        self.messages.addNumbersInToField([self.phone_number])
        self.messages.enterSMSMsg(self.test_msg)
        self.messages.createMMSImage()
        self.gallery.clickThumbMMS(0)

        time.sleep(2)
        self.messages.createMMSMusic()
        self.music.click_on_song_mms()

        self.messages.sendSMS()

        self.UTILS.statusbar.wait_for_notification_toaster_title(self.target_mms_number, timeout=120)
        self.UTILS.statusbar.click_on_notification_title(
            self.target_mms_number, frame_to_change=DOM.Messages.frame_locator, timeout=30)

        self.messages.verifyMMSReceived("img", self.target_mms_number)
        self.messages.verifyMMSReceived("audio", self.target_mms_number)
