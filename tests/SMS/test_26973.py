#===============================================================================
# 26973: Click on an email address and Add to an existing contact with 3
# emails address added
#
# Procedure:
# 1. Send a sms from "device A" to "device B" who contains an email address
# 2. Open sms app in the device A.
# 3. Hold on the email address contained in the sms
# 4. Click on "Add to existing contact" button
# 5. Select a contact with 3 emails address inserted
# 5. Insert contact photo, name, surname, company, phone number, address
# comment and other email addrees.
# 6. Press save button
#
# Expected results:
# Contact is saved and The user returns to sms app in the conversation screen
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    test_msg = "Test message."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.email_address = self.UTILS.general.get_os_variable("GMAIL_1_EMAIL")

        self.cont = MockContact(email=[{"type": "Personal", "value": "email1@nowhere.com"},
                               {"type": "Personal", "value": "email2@nowhere.com"},
                               {"type": "Personal", "value": "email3@nowhere.com"}])
        self.UTILS.general.insertContact(self.cont)

        self.UTILS.general.add_file_to_device('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.phone_number], "Hello {} old bean.".format(self.email_address))
        send_time = self.messages.last_sent_message_timestamp()
        msg = self.messages.wait_for_message(send_time=send_time)

        #
        # Press the email link.
        #
        link = msg.find_element("tag name", "a")
        link.tap()

        #
        # Click 'Add to an existing contact'.
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_add_to_contact_btn, "Add to an existing contact button")
        x.tap()

        #
        # Verify that the email is in the email field.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        contact = self.UTILS.element.getElement(DOM.Contacts.contact_names, "Contact name in search page")
        contact.tap()

        self.UTILS.element.waitForElements(("xpath",
                                "//input[@type='email' and @value='{}']".format(self.email_address)),
                                "New email address")

        #
        # Add gallery image.
        #
        self.contacts.add_gallery_image_to_contact(0)

        #
        # Press the Update button.
        #
        done_button = self.UTILS.element.getElement(DOM.Contacts.edit_update_button, "'Update' button")
        done_button.tap()

        #
        # Check that the contacts iframe is now gone.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@src,'contacts')]"),
                                       "Contact app iframe")

        #
        # Now return to the SMS app.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
