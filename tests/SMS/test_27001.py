#
# 27001
#
from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.incoming_sms_num = self.UTILS.general.get_os_variable("GLOBAL_CP_NUMBER").split(',')

        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()
        self.messages.deleteAllThreads()
        #
        # Create and send a new test message.
        #
        msg_text = "Nine 111111111 numbers."
        self.UTILS.messages.create_incoming_sms(self.phone_number, msg_text)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(msg_text, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.incoming_sms_num, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)
        sms = self.messages.lastMessageInThisThread()

        #
        # Long press the embedded number link.
        #
        num = sms.find_element("tag name", "a")
        num.tap()

        #
        # Select add to existing contact.
        #
        add_btn = self.UTILS.element.getElement(DOM.Messages.header_add_to_contact_btn,
                                    "Add to existing contact button")
        add_btn.tap()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        #
        # Select our contact.
        #
        self.contacts.view_contact(self.contact["familyName"], False)

        #
        # Check the phone number.
        #
        num = self.UTILS.element.getElement(("id", "number_1"), "2nd phone number.")
        self.UTILS.test.TEST(num.get_attribute("value") == "111111111",
                        "Contact now has a 2nd number which is '111111111' (it was '{}').".\
                        format(num.get_attribute("value")))

        #
        # Press the update button.
        #
        update_btn = self.UTILS.element.getElement(DOM.Contacts.edit_update_button, "Update button")
        update_btn.tap()

        #
        # Wait for contacts app to close and return to sms app.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@src, '{}')]".\
                                               format(DOM.Contacts.frame_locator[1])), "Contacts iframe")

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
