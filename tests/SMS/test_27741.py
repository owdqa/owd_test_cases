from gaiatest import GaiaTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages

class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        # Import contact (adjust to the correct number).
        self.telNum = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Using target telephone number " + self.telNum)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()
        """
        Send a message to create a thread (use number, not name as this
        avoids some blocking bugs just now). 
        """

        self.messages.create_and_send_sms([self.telNum], "Test message.")
        returnedSMS = self.messages.wait_for_message()

