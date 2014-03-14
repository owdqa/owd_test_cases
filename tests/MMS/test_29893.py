#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps import Settings

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
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending mms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Turn on 3g connection.
        #
        self.Settings.turn_dataConn_on()

        #
        # Create and Send an MMS
        #
        self.messages.createAndSendMMS("image", self.test_msg)
         #
        # Verify that the MMS has been received.
        #
        self.messages.verifyMMSReceived("image")

