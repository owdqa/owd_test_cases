#===============================================================================
# 26974: Click on an email address and Add to an existing contact without email
# address added
#
# Procedure:
# 1. Send a sms from "device A" to "device B" who contains an email address
# 2. Open sms app in the device A.
# 3. Hold on the email address contained in the sms
# 4. Click on "Add to existing contact" button
# 5. Select a contact without email address inserted
# 5. Insert contact photo, name, surname, company, phone number, address
# comment and other email address.
# 6. Press save button
#
# Expected results:
# Contact is created and The user returns to sms app in the conversation screen
#===============================================================================

from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact
import time


class test_main(GaiaTestCase):

    link = "owdqatestone@gmail.com"
    test_msg = "Test " + link + " this."

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        # Insert a contact without email addresses
        self.UTILS.general.add_file_to_device('./tests/_resources/contact_face.jpg')
        self.contact = MockContact(email={'type': 'Personal', 'value': ''})

        self.UTILS.general.insertContact(self.contact)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.general.remove_files()
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()

        # Create and send a new test message.
        self.messages.create_and_send_sms([self.phone_number], self.test_msg)
        """
        Wait for the last message in this thread to be a 'received' one
        and click the link.
        """

        x = self.messages.wait_for_message()
        self.UTILS.test.test(x, "Received a message.", True)

        a = x.find_element("tag name", "a")

        a.tap()

        # Press 'add to existing contact' button.
        w = self.UTILS.element.getElement(DOM.Messages.header_add_to_contact_btn,
                                    "Add to existing contact button")
        w.tap()

        # Switch to Contacts app.
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        # Select the contact.
        prepopulated_contact = (DOM.Contacts.view_all_contact_specific_contact[0],
                                DOM.Contacts.view_all_contact_specific_contact[1].format("OWD"))

        contact = self.UTILS.element.getElement(prepopulated_contact, "Search item")
        contact.tap()

        # Fill out all the other details.
        contFields = self.contacts.get_contact_fields()
        """
        Put the contact details into each of the fields (this method
        clears each field first).
        """

        self.contacts.replace_str(contFields['givenName'], self.contact["givenName"] + "bis")
        self.contacts.replace_str(contFields['familyName'], self.contact["familyName"] + "bis")
        self.contacts.replace_str(contFields['tel'], self.contact["tel"]["value"] + "bis")
        self.contacts.replace_str(contFields['street'], self.contact["addr"]["streetAddress"] + "bis")
        self.contacts.replace_str(contFields['zip'], self.contact["addr"]["postalCode"] + "bis")
        self.contacts.replace_str(contFields['city'], self.contact["addr"]["locality"] + "bis")
        self.contacts.replace_str(contFields['country'], self.contact["addr"]["countryName"] + "bis")
        self.contacts.add_gallery_image_to_contact(0)

        # Add another email address.
        self.contacts.add_another_email_address(self.contact["email"]["value"])

        # Press the Done button.
        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()

        # Check that the contacts iframe is now gone.
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@src,'contacts')]"), "Contact app iframe")

        # Now return to the SMS app.
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
