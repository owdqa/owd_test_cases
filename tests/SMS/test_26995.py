from gaiatest import GaiaTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        test_str = "Four 1234 six 123456 seven 1234567 eight 12345678 nine 123456789 numbers."
        self.messages.create_and_send_sms([self.phone_number], test_str)
        x = self.messages.wait_for_message()

        #
        # Check how many are links.
        #
        fnam = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot (for reference):", fnam)

        y = x.find_elements("tag name", "a")  

        bool4OK = True
        bool6OK = True
        for i in y:
            self.UTILS.reporting.logResult("info", "FYI: {} is highlighted.".format(i.text))
            if i.text == "1234":
                bool4OK = False
            if i.text == "123456":
                bool7OK = False

        self.UTILS.test.test(bool4OK, "The 4-digit number is not highlighted.")
        self.UTILS.test.test(bool6OK, "The 6-digit number is not highlighted.")

        