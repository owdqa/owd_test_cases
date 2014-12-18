#
# TC_MMSTC_COMPT_010d
# Message with text, audio and images
from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.music import Music
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    test_msg = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)
        self.music = Music(self)
        self.settings = Settings(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.general.remove_files()
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        #
        # Load files into the device.
        #
        self.UTILS.general.add_file_to_device('./tests/_resources/imgd.jpg')
        self.UTILS.general.add_file_to_device('./tests/_resources/MP3.mp3')

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

        self.messages.create_mms_image()
        self.gallery.click_on_thumbnail_at_position_mms(0)

        self.messages.create_mms_music()
        self.music.click_on_song_mms()

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()
        self.messages.wait_for_message()
        self.messages.verify_mms_received('img', self.phone_number)
        self.messages.verify_mms_received('audio', self.phone_number)
