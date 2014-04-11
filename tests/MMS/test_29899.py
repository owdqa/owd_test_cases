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
from OWDTestToolkit.apps.settings import Settings

class test_main(GaiaTestCase):

    #
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
        self.Settings = Settings(self)

        self.test_msg = "Hello World"

        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):


        #
        # Configure Auto Retrieve as "on_with_r = On with roaming option" from messaging settings
        #
        self.Settings.configureMMSAutoRetrieve("on_with_r")

        #
        # Set up to use data connection.
        #
        self.messages.createAndSendMMS("image", [self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")], self.test_msg)

        #
        # Verify that the MMS has been received.
        #
        self.messages.verifyMMSReceived("image")