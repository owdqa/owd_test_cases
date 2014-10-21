#
# 27000
#
from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts


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

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Create and send a new test message.
        #
        msg_text = "Nine 123456789 numbers."
        self.UTILS.messages.create_incoming_sms(self.phone_number, msg_text)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(msg_text, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.incoming_sms_num, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)
        sms = self.messages.lastMessageInThisThread()

        #
        # Long press the embedded number link.
        #
        link = sms.find_element("tag name", "a")
        link.tap()

        #
        # Select create new contact.
        #
        btn = self.UTILS.element.getElement(DOM.Messages.header_create_new_contact_btn, "Create new contact button")
        btn.tap()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        contFields = self.contacts.get_contact_fields()

        #
        # Verify the number is in the number field.
        #
        self.UTILS.test.TEST("123456789" in contFields['tel'].get_attribute("value"),
                        "Our target number is in the telephone field (expected {}).".\
                        format(contFields['tel'].get_attribute("value")))

        #
        # Put the contact details into each of the fields (this method
        # clears each field first).
        #
        self.contacts.replace_str(contFields['givenName'], "Test27000")
        self.contacts.replace_str(contFields['familyName'], "Testerton")
        x = self.UTILS.element.getElement(DOM.Contacts.done_button, "Done button")
        x.tap()

        #
        # Wait for the contacts app to go away.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@src, '{}')]".\
                                               format(DOM.Contacts.frame_locator[1])), "Contacts iframe")

        #
        # Verify that the sms app is still running.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
