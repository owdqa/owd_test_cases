#
# TC_MMSTC-FEATR-030a
# Reception of video file + JPG file + AMR file
#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *


class test_main(GaiaTestCase):
    
    _TestMsg     = "Hello World"
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.gallery    = Gallery(self)
        self.music      = Music(self)
        self.video      = Video(self)
        
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
        self.UTILS.addFileToDevice('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')
        self.UTILS.addFileToDevice('./tests/_resources/AMR.amr', destination='/SD/mus')
        self.UTILS.addFileToDevice('./tests/_resources/mpeg4.mp4', destination='/SD/mus')

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
        self.messages.addNumbersInToField([ self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM") ])

        #
        # Create MMS.
        #
        self.messages.enterSMSMsg(self._TestMsg)

        self.messages.createMMSImage()
        self.gallery.clickThumbMMS(0)

        self.messages.createMMSMusic()
        self.music.clickOnSongMMS()

        self.messages.createMMSVideo()
        self.video.clickOnVideoMMS(0)

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()

        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        self.messages.openThread("+" + self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))

        #
        # Wait for the last message in this thread to be a 'recieved' one.
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)