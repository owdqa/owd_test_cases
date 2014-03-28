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
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact
import time


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        #
        # Prepare the contact we're going to insert.
        #
        self.num1 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel = {'type': '', 'value': ''})

        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Type a message containing the required string 
        #
        self.messages.startNewSMS()
        self.messages.enterSMSMsg("Test message")

        #
        # Search for our contact.
        #
        orig_iframe = self.messages.selectAddContactButton()

        #
        # Search the contacts list for our contact.
        #
        x = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        for i in x:
            if i.text == self.contact["name"]:
                self.UTILS.reporting.logResult("info", "Tapping ...")
                i.tap()
                break

        time.sleep(2)

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

        self.messages.checkIsInToField("", True)

        # self.UTILS.element.waitForElements(DOM.Messages.contact_no_phones_msg, "Message saying this contact has no phones")
        # x = self.UTILS.element.getElement(DOM.Messages.contact_no_phones_ok, "OK button")
        # x.tap()
        #
        # self.UTILS.element.headerCheck("Select contact")