#===============================================================================
# 29919: Verify that the user can attach a file .mp4 and it is displayed
# as video
#
# Procedure:
# 1. Open sms app
# 2. press attach button
# 3. Select a file .mp4
# ER1
# 4. Press send button
# ER2
#
# Expected results:
# ER1 The file is attached and is displayed as video in the sms composer
# ER2 The MMS is sends successfully
#===============================================================================
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
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

        self.test_msg = "Hello World"

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.UTILS.general.add_file_to_device('./tests/_resources/mpeg4.mp4', destination='/SD/mus')
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.general.remove_file('mpeg4.mp4', '/SD/mus')
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
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
        self.messages.create_mms_video()
        self.video.click_on_video_at_position_mms(0)
        container = self.UTILS.element.getElement(DOM.Messages.attach_preview_video_audio_type, "Video container")
        self.UTILS.test.test(container.get_attribute("data-attachment-type") == "video", "Video container found")
