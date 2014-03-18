#
# TC_MMSTC_COMPT_010d
# Message with text, audio and images
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
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending mms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):

        #
        # Load files into the device.
        #
        self.UTILS.addFileToDevice('./tests/_resources/imgd.jpg',
                                    destination='DCIM/100MZLLA')
        self.UTILS.addFileToDevice('./tests/_resources/MP3.mp3',
                                    destination='/SD/mus')

        #
        # Activate data connection
        #
        #self.settings.turn_dataConn_on()

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