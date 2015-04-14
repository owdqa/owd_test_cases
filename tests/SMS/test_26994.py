from OWDTestToolkit.firec_testcase import FireCTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages

class test_main(FireCTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        test_str = "Four 1234 seven 1234567 eight 12345678 nine 123456789 numbers."
        self.messages.create_and_send_sms([self.phone_number], test_str)
        x = self.messages.wait_for_message()

        #
        # Check how many are links.
        #
        fnam = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot (for reference):", fnam)

        y = x.find_elements("tag name", "a")  

        bool7OK = False
        bool8OK = False
        bool9OK = False
        for i in y:
            self.UTILS.reporting.logResult("info", "FYI: %s is highlighted." % i.text)
            if i.text == "1234567":
                bool7OK = True
            if i.text == "12345678":
                bool8OK = True
            if i.text == "123456789":
                bool9OK = True

        self.UTILS.test.test(bool7OK, "The 8-digit number is highlighted.")
        self.UTILS.test.test(bool8OK, "The 8-digit number is highlighted.")
        self.UTILS.test.test(bool9OK, "The 9-digit number is highlighted.")

        