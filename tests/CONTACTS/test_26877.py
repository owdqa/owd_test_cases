from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.messages import Messages
import time
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)

        #
        # Prepare the contact we're going to insert.
        #
        tlf = self.UTILS.general.get_config_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel={'type': 'Mobile', 'value': tlf})

        #
        # Establish which phone number to use.
        #
        self.num2 = "123456789"

        #
        # Add this contact (quick'n'dirty method - we're just testing sms, no adding a contact).
        #
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Create a thread for this contact.
        #
        #(Just so we can switch to it later)
        self.contacts.launch()
        self.messages.launch()

        self.messages.create_and_send_sms([self.contact["tel"]["value"]], "Test message")
        self.messages.wait_for_message()

        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        self.messages.create_and_send_sms([self.num2], "Thread for a different number")

        self.UTILS.reporting.logResult("info", " ")
        self.UTILS.reporting.logResult("info", "=================================================================")
        self.UTILS.reporting.logResult("info", "<b>If SMS app is closed when you click 'send sms' in contacts ...</b>")
        self._doTest()

        self.UTILS.reporting.logResult("info", " ")
        self.UTILS.reporting.logResult("info", "=====================================================================")
        self.UTILS.reporting.logResult("info", "<b>If SMS app is still open when you click 'send sms' in contacts ...</b>")
        self.messages.openThread(self.num2)
        self._doTest()

    def _doTest(self):
        #
        # Launch contacts app etc...
        #
        self.UTILS.app.switchToApp("Contacts")
        self.contacts.view_contact(self.contact['name'], False)
        smsBTN = self.UTILS.element.getElement(DOM.Contacts.sms_button, "Send SMS button")
        smsBTN.tap()

        #
        # Switch to sms frame and complete the tests + send the message.
        #
        time.sleep(5)
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        self.UTILS.reporting.logResult("info", "<b>NOTE: </b>expecting to be in a 'compose new sms' screen (not a thread) ...")

        self.messages.enterSMSMsg("Test msg.")
        self.messages.sendSMS()

        #
        # Verify that we are now in the thread for this contact.
        #
        self.UTILS.reporting.logResult("info",
                             "<b>NOTE: </b> expecting to be automatically taken to the thread for '{}' ...".\
                             format(self.contact['name']))

        msg_count = self.UTILS.element.getElements(DOM.Messages.message_list, "Thread messages", False, 5, False)

        if msg_count:
            self.UTILS.test.test(len(msg_count) > 1, "There are <i>some</i> messages in this thread already.")
        else:
            self.UTILS.reporting.logResult(False, "There are <i>some</i> messages in this thread already.")
