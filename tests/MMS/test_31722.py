#
# TC_MMSTC_PREST_008a
# Hyperlinks
#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.browser import Browser
import time


class test_main(GaiaTestCase):

    link1 = "www.google.com"
    test_msg = "Open this URL: " + link1

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)
        self.browser = Browser(self)

        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.target_mms_number = self.UTILS.general.get_os_variable("TARGET_MMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        self.UTILS.network.getNetworkConnection()

        #
        # Load sample image into the gallery.
        #
        self.UTILS.general.addFileToDevice('./tests/_resources/imgd.jpg', destination='DCIM/100MZLLA')

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

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()

        time.sleep(2)

        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        self.messages.openThread(self.target_mms_number)

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
        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)

        self.UTILS.test.TEST(self.browser.check_page_loaded(self.link1), "Web page loaded correctly.")
