#===============================================================================
# 29902: MMS received with auto retrieve and when roaming disabled (data connection and wifi available)
#
# Pre-requisites:
# Data connection and wifi enabled, phone is in home network
#
# Procedure:
# 1. Open settings -> Message settings
# 2. Tap on Auto retrieve options
# 3. Select "Off"
# 4. Tap on OK
# 5. Send an MMS to that phone
#
# Expected result:
# 1. Open message settings
# 2. Menu to select Auto retrieve options is displayed
# 4. Back to Message settings
# 5. User receives notification of MMS available
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    # Restart device to starting with wifi and 3g disabled.
    #
    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)
        self.settings = Settings(self)

        self.test_msg = "Hello World"

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.mms_sender = self.UTILS.general.get_os_variable("TARGET_MMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.general.connect_to_cell_data()
        self.data_layer.connect_to_wifi()

        #
        # Configure Auto Retrieve as off from messaging settings
        #
        self.settings.configureMMSAutoRetrieve("off")

        self.messages.createAndSendMMS("image", [self.phone_number], self.test_msg)
        self.marionette.find_element(*DOM.Messages.header_back_button).tap()
        self.UTILS.statusbar.wait_for_notification_toaster_title(self.mms_sender, DOM.Messages.frame_locator,
                                                                 timeout=120)

        #
        # Verify that the MMS has been received, but it contains no attached file
        #
        self.messages.openThread(self.mms_sender)
        last_msg = self.messages.lastMessageInThisThread()
        btn_dl = self.marionette.find_element(*DOM.Messages.button_download_attachment, id=last_msg.id)
        self.UTILS.test.TEST(btn_dl, "Download attachment button present")
