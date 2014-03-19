#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact
import time

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
        self.num1 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel = {'type': '', 'value': self.num1})

        self.UTILS.general.insertContact(self.contact)
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact["tel"]["value"])

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
        self.contacts.viewContact(self.contact['name'])

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
        self.UTILS.test.TEST(returnedSMS, "A receieved message appeared in the thread.", True)

        #
        # TEST: The returned message is as expected (caseless in case user typed it manually).
        #
        sms_text = returnedSMS.text
        self.UTILS.test.TEST((sms_text.lower() == self.test_msg.lower()), 
            "SMS text = '" + self.test_msg + "' (it was '" + sms_text + "').")

        #
        # Examine the carrier.
        #  
        expect = self.contact["tel"]["type"]
        actual = self.messages.threadType()
        self.UTILS.test.TEST(expect == actual, "The type is listed as: '" + expect + "' (subheader was '" + actual + "').")
   
        # 
        # Phone Number is shown instead of carrier as the secondary header
        #
        expect = self.contact["tel"]["value"]
        actual = self.messages.threadCarrier()
        self.UTILS.test.TEST(expect == actual, "The telephone number is: '" + expect + "' (subheader was '" + actual + "').")