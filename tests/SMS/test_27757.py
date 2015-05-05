from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages

class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        # Import contact (adjust the correct number).
        self.telNum = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Using target telephone number " + self.telNum)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()
        """
        Send a message to create a thread (use number, not name as this
        avoids some blocking bugs just now). 
        """

        self.messages.create_and_send_sms([self.telNum], "Test message.")
        returnedSMS = self.messages.wait_for_message()

        # Examine the header.
        self.UTILS.element.headerCheck(self.telNum)

        # Close the thread and check we can find it again with this number.
        self.messages.closeThread()
        self.messages.openThread(self.telNum)
