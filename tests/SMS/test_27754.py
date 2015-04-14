#
# 27754: Send a SMS to multiple contacts
#
import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(FireCTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)

        #
        # Establish which phone number to use and set up the contacts.
        #
        self.test_contacts = [MockContact() for i in range(2)]
        self.test_contacts[0]['tel']['value'] = self.UTILS.general.get_config_variable("phone_number", "custom")
        map(self.UTILS.general.insertContact, self.test_contacts)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # First, we need to make sure there are no statusbar notifications.
        #
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        #
        # Now create and send a SMS to both contacts.
        #
        self.messages.launch()
        self.messages.startNewSMS()

        for i in range(len(self.test_contacts)):
            self.messages.selectAddContactButton()
            self.contacts.view_contact(self.test_contacts[i]["name"], False)
            self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
            self.messages.checkIsInToField(self.test_contacts[i]["name"], True)

        test_msg = "Test message."
        self.messages.enterSMSMsg(test_msg)
        time.sleep(2)
        self.messages.sendSMS(check=False)

        # Since the destination number is the own, we will only receive one message, so we check it once
        self.UTILS.statusbar.wait_for_notification_toaster_detail(test_msg, timeout=120)

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

        # We will also check there is one thread for each contact in the To field
        name_xpath = DOM.Messages.thread_selector_xpath.format(self.test_contacts[0]['name'])
        thread = self.UTILS.element.getElementByXpath(name_xpath)
        self.UTILS.test.test(thread, "Thread for {} found".format(self.test_contacts[0]['name']))
        name_xpath = DOM.Messages.thread_selector_xpath.format(self.test_contacts[1]['name'])
        thread = self.UTILS.element.getElementByXpath(name_xpath)
        self.UTILS.test.test(thread, "Thread for {} found".format(self.test_contacts[1]['name']))
