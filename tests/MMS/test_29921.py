#===============================================================================
# 29921: Verify that the user can receive attached a file .jpg in a MMS and it
# is displayed as image
#
# Procedure:
# 1 Send a mms with a file .jpg attached to a test device
# ER1
# 2. Open the received MMS in the test device
# 3. Open the file received attached in the mms
# ER2
#
# Expected results:
# ER1 The MMS is received in the test device
# ER2 The MMS and the attached filed can be opened.
#===============================================================================

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)

        self.test_msg = "Hello World"

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Create and Send an MMS with a image attached.
        self.messages.create_and_send_mms("image", [self.phone_number], self.test_msg)

        self.messages.wait_for_message()
        self.messages.verify_mms_received("img", self.phone_number)
