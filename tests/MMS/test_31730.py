#
# TC_MMSTC-FEATR-030a
# Reception of video file + JPG file + AMR file
#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.music import Music
from OWDTestToolkit.apps.video import Video

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
        self.video = Video(self)
        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending mms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):

        #
        # Load files into the device.
        #
        self.UTILS.addFileToDevice('./tests/_resources/80x60.jpg',
                                    destination='DCIM/100MZLLA')
        self.UTILS.addFileToDevice('./tests/_resources/AMR.amr',
                                    destination='/SD/mus')
        self.UTILS.addFileToDevice('./tests/_resources/mpeg4.mp4',
                                    destination='/SD/mus')

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
        self.messages.addNumbersInToField([self.target_telNum])

        #
        # Create MMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        self.messages.createMMSImage()
        self.gallery.clickThumbMMS(0)

        self.messages.createMMSMusic()
        self.music.click_on_song_mms()

        self.messages.createMMSVideo()
        self.video.clickOnVideoMMS(0)

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()

        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        self.messages.openThread("+" + self.target_telNum)

        #
        # Wait for the last message in this thread to be a 'recieved' one.
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)