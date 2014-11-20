#===============================================================================
# 29896: Send a MMS when data and wifi are off
#
# Pre-requisites:
# Commercial SIM card needed
#
# Procedure:
# 1. Open messaging app
# 2. Create a new MMS
# 3. Tap on send
#
# Expected results:
# Two expected behaviours depending on the country's apn configuration:
# 1. The MMS is sent
# 2. There is a pop up asking to activate data to send the message, after accepting
# the message is sent
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery


class test_main(GaiaTestCase):

    # Restart device to starting with wifi and 3g disabled.
    #
    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)

        self.test_msg = "Hello World"

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Create and Send an MMS
        #
        self.messages.create_and_send_mms("image", [self.phone_number], self.test_msg)

        #
        # Verify that the MMS has been received.
        #
        self.messages.wait_for_message()
        self.messages.verify_mms_received("img", self.phone_number)
