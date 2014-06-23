#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
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
        msgApp = self.messages.launch()
        self.messages.startNewSMS()
        self.messages.addNumbersInToField([self.num])
        self.messages.enterSMSMsg("Test")
        sendBtn = self.UTILS.element.getElement(DOM.Messages.send_message_button, "Send sms button")
        sendBtn.tap()

        self.apps.kill(msgApp)

        self.browser.launch()
        self.messages.waitForSMSNotifier(self.num, 60)

        self.browser.open_url("www.wikipedia.com")
