#
# 27749: Receive an SMS with a phone number and store it
#
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer


class test_main(GaiaTestCase):

    test_num = "089123456"
    test_msg = "Testing " + test_num + " number."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.Dialer = Dialer(self)
        self.contacts = Contacts(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.cp_incoming_number = self.UTILS.general.get_config_variable("sms_platform_numbers", "common").split(',')
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.connect_to_network()
        self.UTILS.statusbar.clearAllStatusBarNotifs()
        #
        # Launch messages app.
        #
        self.messages.launch()

        self.UTILS.messages.create_incoming_sms(self.phone_number, self.test_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.cp_incoming_number, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)

        last_msg = self.messages.last_message_in_this_thread()
        num = last_msg.find_element("tag name", "a")
        num.tap()

        call_btn = self.UTILS.element.getElement(DOM.Messages.header_call_btn, "Call button")
        call_btn.tap()

        time.sleep(5)

        #
        # Create a contact from this number.
        #
        self.Dialer.createContactFromThisNum()

        #
        # Make sure the number is automatically in the contact details.
        #
        number_field = self.UTILS.element.getElement(("id", "number_0"), "Mobile number field")
        self.UTILS.test.test(number_field.get_attribute("value") == self.test_num,
                        "The correct number is automatically entered in the new contact's number field.")
