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
        # Establish which phone number to use and set up the contacts.
        #
        self.nums = [self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM"),
                        self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM_SHORT")]

        self.test_contacts = [MockContact(tel={'type': 'Mobile', 'value': self.nums[i]}) for i in range(2)]
        map(self.UTILS.general.insertContact, self.test_contacts)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # First, we need to make sure there are no statusbar notifs.
        #
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        #
        # Now create and send an sms to both contacts.
        #
        self.messages.launch()
        self.messages.startNewSMS()

        for i in range(len(self.test_contacts)):
            self.messages.selectAddContactButton()
            self.contacts.view_contact(self.test_contacts[i]["name"], False)
            self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
            self.messages.checkIsInToField(self.test_contacts[i]["name"], True)

        self.messages.enterSMSMsg("Test message.")
        self.messages.sendSMS()

        self.UTILS.statusbar.wait_for_notification_toaster_title(self.nums[0], timeout=120)
        self.UTILS.statusbar.wait_for_notification_toaster_title(self.nums[1], timeout=120)
