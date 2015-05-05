from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages

class test_main(SpreadtrumTestCase):

    test_str = "abcdefghijklmnopqrstuvwxyz"

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()
        """
        Type a message containing the required string 
        (the test is already included in 'enterSMSMsg' because it uses 'typeThis()').
        """

        self.messages.startNewSMS()

        self.messages.enterSMSMsg(self.test_str, False)

        self.UTILS.debug.screenShot("5968")



