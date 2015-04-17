#===============================================================================
# 26849: Receive sms while the user is in the SMS app (vibration alert)
#
# Procedure:
# 1- Send a SMS to our device
#
# Expected result:
# The SMS is received with the correct notification
#===============================================================================

from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.msg = "Test {}".format(time.time())
        self.cp_incoming_number = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        self.UTILS.messages.create_incoming_sms(self.phone_number, self.msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.msg, timeout=120)
