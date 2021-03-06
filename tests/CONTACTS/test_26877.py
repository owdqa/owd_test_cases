import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)

        tlf = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.contact = MockContact(tel={'type': 'Mobile', 'value': tlf})
        self.num2 = "123456789"

        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # Create a thread for this contact.
        # (Just so we can switch to it later)
        self.messages.launch()
        self.messages.create_and_send_sms([self.contact["tel"]["value"]], "Test message")
        self.messages.wait_for_message()
        self.messages.go_back()
        self.messages.create_and_send_sms([self.num2], "Thread for a different number")

        self.apps.kill_all()
        time.sleep(2)

        self.UTILS.reporting.logResult("info", "<b>If SMS app is closed when you click 'send sms' in contacts ...</b>")
        self._doTest()

        self.apps.kill_all()
        time.sleep(2)
        self.messages.launch()
        self.UTILS.reporting.logResult(
            "info", "<b>If SMS app is still open when you click 'send sms' in contacts ...</b>")
        self.messages.openThread(self.num2)
        self._doTest()

    def _doTest(self):
        # Launch contacts app etc...
        self.contacts.launch()
        self.contacts.view_contact(self.contact['name'], False)
        smsBTN = self.UTILS.element.getElement(DOM.Contacts.sms_button, "Send SMS button")
        smsBTN.tap()

        # Switch to sms frame and complete the tests + send the message.
        time.sleep(5)
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        self.UTILS.reporting.logResult(
            "info", "<b>NOTE: </b>expecting to be in a 'compose new sms' screen (not a thread) ...")

        self.messages.enterSMSMsg("Test msg.")
        self.messages.sendSMS()

        # Verify that we are now in the thread for this contact.
        self.UTILS.reporting.logResult("info",
                                       "<b>NOTE: </b> expecting to be automatically taken to the thread for '{}' ...".
                                       format(self.contact['name']))

        msg_count = self.UTILS.element.getElements(DOM.Messages.message_list, "Thread messages", False, 5, False)

        if msg_count:
            self.UTILS.test.test(len(msg_count) > 1, "There are <i>some</i> messages in this thread already.")
        else:
            self.UTILS.reporting.logResult(False, "There are <i>some</i> messages in this thread already.")
