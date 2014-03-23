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
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.messages import Messages
import time
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    test_msg = "Test."

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
        tel = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        self.contact_1 = MockContact(tel={'type': 'Mobile', 'value': tel})

        #
        # Establish which phone number to use.
        #
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact_1["tel"]["value"])

        #
        # Import this contact (quick'n'dirty method - we're just testing sms, no adding a contact).
        #
        self.UTILS.general.insertContact(self.contact_1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # View the details of our contact.
        #
        self.contacts.view_contact(self.contact_1['name'])

        #
        # Tap the sms button in the view details screen to go to the sms page.
        #
        smsBTN = self.UTILS.element.getElement(DOM.Contacts.sms_button, "Send SMS button")
        smsBTN.tap()

        #
        # Switch to the 'Messages' app frame (or marionette will still be watching the
        # 'Contacts' app!).
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

        #
        # Create SMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Click send.
        #
        self.messages.sendSMS()

        #
        # Wait for the last message in this thread to be a 'recieved' one.
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.test.TEST(returnedSMS, "A received message appeared in the thread.", True)

        #
        # TEST: The returned message is as expected (caseless in case user typed it manually).
        #
        sms_text = returnedSMS.text
        self.UTILS.test.TEST((sms_text.lower() == self.test_msg.lower()),
                        "SMS text = '{}' (it was '{}').".format(self.test_msg, sms_text))
