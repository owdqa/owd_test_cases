#===============================================================================
# 31722: Hyperlinks
#
# Pre-requisites:
# Client A and B support Hyperlinks embedded in MMs
# Client B supports browser
#
# Procedure:
# Verify that the MMS client can add hyperlinks in an MM and that the recipient
# MMS client recognizes the hyperlinks and allows the user to follow it on demand.
# 1. In client A, compose an MM including a hyperlink at any point in the MM
# 2. In client A, send the MM to client B
# 3. In client B, retrieve the message
# 4. In client B, display the message
# 5. In client B, select the hyperlink and request to follow it
#
# Expected results:
# In client A, a hyperlink can be inserted in the MM
# In client B, the message is displayed correctly. Client B recognizes the hyperlink
# and gives the user the option to follow it on demand. The hyperlink is not followed
# unless the user requests it explicitly. If the user requests to follow the hyperlink,
# the browser is opened and the URL of the hyperlink is displayed"
#===============================================================================

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
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.target_mms_number = self.UTILS.general.get_os_variable("TARGET_MMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.connect_to_cell_data()

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
        self.messages.addNumbersInToField([self.phone_number])

        #
        # Create MMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        self.messages.createMMSImage()
        self.gallery.click_on_thumbnail_at_position_mms(0)

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()
        self.UTILS.statusbar.wait_for_notification_toaster_title(self.target_mms_number, timeout=120)
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        self.messages.openThread(self.target_mms_number)

        #
        # Find all URLs
        #
        x = self.messages.lastMessageInThisThread()
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
