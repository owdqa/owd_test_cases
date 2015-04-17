#===============================================================================
# 29920: Verify that the user can attach a file .mp3 and it is displayed
# as audio
#
# Procedure:
# 1. Open sms app
# 2. press attach button
# 3. Select a file .mp3
# ER1
# 4. Press send button
# ER2
#
# Expected results:
# ER1 The file is attached and is displayed as audio in the sms composer
# ER2 The MMS is sends successfully
#===============================================================================

from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.music import Music


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.music = Music(self)

        self.test_msg = "Hello World"

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.UTILS.general.add_file_to_device('./tests/_resources/MP3.mp3', destination='/SD/mus')
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.general.remove_file('MP3.mp3', '/SD/mus')
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

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
        self.messages.create_mms_music()
        self.music.click_on_song_mms()
        container = self.UTILS.element.getElement(DOM.Messages.attach_preview_video_audio_type, "Audio container")
        self.UTILS.test.test(container.get_attribute("data-attachment-type") == "audio", "Audio container found")
