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
#import time

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
        msgapp = self.messages.launch()
        self.messages.createAndSendSMS([self.num1], "Test")
        self.messages.waitForReceivedMsgInThisThread()

        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        self.messages.openThread(self.contact["name"])

        #
        # Delete the contact
        #
        self.apps.kill(msgapp)
        self.contacts.launch()
        self.contacts.deleteContact(self.contact["name"])

        #
        # Go back to SMS app and try to open the thread by phone number
        #
        self.messages.launch()
        self.messages.openThread(self.contact["tel"]["value"])

