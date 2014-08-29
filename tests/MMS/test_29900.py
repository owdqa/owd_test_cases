#===============================================================================
# 29900: MMS received with auto retrieve and when roaming enabled (data and wifi
#       connection available)
#
# Pre-requisites:
# Data connection and wifi enabled, phone is in home network
#
# Procedure:
# 1. Open settings -> Message settings
# 2. Select "On with roaming"
# 3. Tap on OK
# 4. Send an MMS to that phone
#
# Expected results:
# 1. Open message settings
# 2. Roamin option is enabled
# 3. Back to Message settings
# 4. The MMS is received ok
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
        # Configure Auto Retrieve as "on_with_r = On with roaming option" from messaging settings
        #
        self.settings.configureMMSAutoRetrieve("on_with_r")

        self.messages.createAndSendMMS("image", [self.phone_number], self.test_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_title(self.mms_sender, DOM.Messages.frame_locator,
                                                                 timeout=120)
        self.marionette.find_element(*DOM.Messages.header_back_button).tap()
        #
        # Verify that the MMS has been received.
        #
        self.messages.verifyMMSReceived("img", self.mms_sender)
