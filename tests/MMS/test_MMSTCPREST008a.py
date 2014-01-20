#
# TC_MMSTC_PREST_008a
# Hyperlinks
#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *


class test_main(GaiaTestCase):
    
    _link1        = "www.google.com"
    _TestMsg     = "Open this URL: " + _link1
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.gallery    = Gallery(self)
        self.browser    = Browser(self)
        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending mms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.UTILS.getNetworkConnection()

        #
        # Load sample image into the gallery.
        #
        self.UTILS.addFileToDevice('./tests/_resources/imgd.jpg', destination='DCIM/100MZLLA')

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

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()

        time.sleep(2)

        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        self.messages.openThread("+" + self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))

        #
        # Find all URLs
        #
        x = self.messages.waitForReceivedMsgInThisThread()
        y = x.find_elements("tag name", "a")

        #
        # Tap on required link.
        #
        y[0].tap()

        #
        # Give the browser time to start up, then
        # switch to the browser frame and check the page loaded.
        #
        time.sleep(3)
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)

        self.UTILS.TEST(self.browser.check_page_loaded(self._link1),
                 "Web page loaded correctly.")
