#===============================================================================
# 29901: MMS received with auto retrieve and when roaming disabled (data connection
#       not available)
#
# Pre-requisites:
# Data connection and wifi disabled, phone is in home network
#
# Procedure:
# 1. Open settings -> Message settings
# 2. Tap on Auto retrieve options
# 3. Select "Off"
# 4. Tap on OK
# 5. Send an MMS to that phone
#
# Expected results:
# 1. Open message settings
# 2. Menu to select Auto retrieve options is displayed
# 3. Back to Message settings
# 4. User receives notification of MMS available
#===============================================================================

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.settings import Settings


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)
        self.settings = Settings(self)

        self.test_msg = "Hello World"

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Configure Auto Retrieve as off from messaging settings
        self.settings.launch()
        self.settings.configure_mms_auto_retrieve("on_without_r")

        send_time = self.messages.create_and_send_mms("image", [self.phone_number], self.test_msg)
        self.messages.wait_for_message(send_time)
        self.messages.verify_mms_received("img", self.phone_number)
