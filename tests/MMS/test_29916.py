#===============================================================================
# 29916: Verify that the user can delete all MMS in a thread with an unsent MMS
#
# Procedure:
# 1. Open SMS app
# 2. Open edit mode
# 3. Press select all button
# 4. Press delete button
#
# Expected results:
# All MMS are removed
#===============================================================================

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)

        timestamp = time.time()
        self.test_msgs = ["Hello world {} at {}".format(i, timestamp) for i in range(3)]

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        for msg in self.test_msgs:
            self.messages.create_and_send_mms("image", [self.phone_number], msg)
            self.messages.wait_for_message()
            self.messages.closeThread()

        self.messages.openThread(self.phone_number)
        self.messages.deleteMessagesInThisThread()
