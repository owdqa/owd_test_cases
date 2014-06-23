#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.messages import Messages


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.browser = Browser(self)
        self.messages = Messages(self)

        self.num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.data_layer.connect_to_wifi()

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Open the browser app.
        #
        self.browser.launch()

        #
        # Open our URL.
        #
        self.browser.open_url("www.google.com")

        #
        # Open the SMS app, send a message then jump back to the browser asap.
        #
        self.messages.launch()
        self.messages.createAndSendSMS([self.num], "Test message.")

        self.apps.kill_all()

        self.browser.launch()
        self.browser.open_url("www.wikipedia.com")
