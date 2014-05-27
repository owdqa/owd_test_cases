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
        tlf = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel={'type': 'Mobile', 'value': tlf})

        #
        # Establish which phone number to use.
        #
        self.num2 = "123456789"

        #
        # Add this contact (quick'n'dirty method - we're just testing sms, no adding a contact).
        #
        self.UTILS.general.insertContact(self.contact)

        #
        # Clean all messages
        #
        self.data_layer.delete_all_sms()

        #
        # Send an sms to num2 so that we have more than a thread
        #
        self.data_layer.send_sms(self.num2, "Dummy message for num2")

        #
        # Send an sms to the contact's number, so that we leave the thread opened
        #
        self.data_layer.send_sms(self.contact["tel"]["value"], "Previous message for contact's number")
        #
        # Wait for the last message in this thread to be a 'received' one.
        #
        self.UTILS.statusbar.wait_for_notification_toaster_title(self.contact["name"], timeout=120)
        # self.UTILS.statusbar.click_on_notification_title(self.contact["name"], DOM.Messages.frame_locator)
        time.sleep(5)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        self.contacts.launch()

        self.contacts.view_contact(self.contact['name'], False)
        smsBTN = self.UTILS.element.getElement(DOM.Contacts.sms_button, "Send SMS button")
        smsBTN.tap()

        #
        # Switch to sms frame and complete the tests + send the message.
        #
        time.sleep(5)

        #
        # It seems that when trying to send a message from contacts application, a new activity
        # is created, so that it won't be seen if we switch to DOM.Messages.frame_locator
        # Therefore, we have to switch to the frame of that new activity.
        #
        self.UTILS.iframe.switchToFrame(*('src', 'activity-new'))
        self.UTILS.reporting.logResult("info", "<b>NOTE: </b>expecting to be in a 'compose new sms' screen (not a thread) ...")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of SMS:", x)

        # self.messages.enterSMSMsg("Test msg.")
        input_field = self.UTILS.element.getElement(DOM.Messages.input_message_area, "input area")
        input_field.send_keys("Writing message from contacts")
        self.messages.sendSMS()
        self.UTILS.statusbar.wait_for_notification_toaster_title(self.contact["name"], timeout=120)

        #
        # Verify that we are now in the thread for this contact.
        #
        self.UTILS.reporting.logResult("info",
                             "<b>NOTE: </b> expecting to be automatically taken to the thread for '{}' ...".\
                             format(self.contact['name']))

        msg_count = self.UTILS.element.getElements(DOM.Messages.message_list, "Thread messages", False, 5, False)

        if msg_count:
            self.UTILS.test.TEST(len(msg_count) > 1, "There are <i>some</i> messages in this thread already.")
        else:
            self.UTILS.reporting.logResult(False, "There are <i>some</i> messages in this thread already.")