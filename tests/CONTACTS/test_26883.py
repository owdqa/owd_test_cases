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
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.messages import Messages
import time
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    test_msg = "Test."
    restart_device = True

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
        tlf = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel={'type': 'Mobile', 'value': tlf})

        self.UTILS.logComment("Using target telephone number " + self.contact["tel"]["value"])

        #
        # Add this contact (quick'n'dirty method - we're just testing sms, no adding a contact).
        #
        self.UTILS.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # View the details of our contact.
        #
        self.contacts.view_contact(self.contact['name'])

        #
        # Tap the sms button in the view details screen to go to the sms page.
        #
        smsBTN = self.UTILS.getElement(DOM.Contacts.sms_button, "Send SMS button")
        smsBTN.tap()

        #
        # Switch to the 'Messages' app frame (or marionette will still be watching the
        # 'Contacts' app!).
        #
        time.sleep(2)
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)

        #
        # Create SMS.
        #
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "frame", x)
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Click send.
        #
        self.messages.sendSMS()
