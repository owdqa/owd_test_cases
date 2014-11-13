#===============================================================================
# 26972: Click on an email address and create a new contact fillings all fields

# Procedure:
# 1. Send a sms from "device A" to "device B" who contains an email address
# 2. Open sms app in the device A.
# 3. Hold on the email address contained in the sms
# 4. Click on "Create new contact" button
# 5. Insert contact photo, name, surname, company, phone number, address comment
# and other email addrees.
# 6. Press save button

# Expected results:
# Contact is created.
# The user return to sms app in the conversation screen.
#===============================================================================

from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.email import Email
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...

        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)
        self.email = Email(self)

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.emailAddy = self.UTILS.general.get_os_variable("GMAIL_1_EMAIL")
        self.emailE = self.UTILS.general.get_os_variable("GMAIL_2_EMAIL")
        self.emailP = self.UTILS.general.get_os_variable("GMAIL_2_PASS")
        self.emailU = self.UTILS.general.get_os_variable("GMAIL_2_USER")

        self.UTILS.general.add_file_to_device('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')
        self.test_msg = "Test message."

        self.cont = MockContact()
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.connect_to_network()

        self.email.launch()
        self.email.setupAccount(self.emailU, self.emailE, self.emailP)

        self.messages.launch()

        # Create and send a new test message.
        self.messages.create_and_send_sms([self.phone_number], "Hello {} old bean.".format(self.emailAddy))
        send_time = self.messages.last_sent_message_timestamp()
        x = self.messages.wait_for_message(send_time=send_time)

        link = x.find_element("tag name", "a")
        link.tap()

        # Click 'create new contact'.
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        x = self.UTILS.element.getElement(DOM.Messages.header_create_new_contact_btn, "Create new contact button")
        x.tap()

        # Verify that the email is in the email field.
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        x = self.UTILS.element.getElement(DOM.Contacts.email_field, "Email field")
        x_txt = x.get_attribute("value")
        self.UTILS.test.test(x_txt == self.emailAddy, "Email is '{}' (expected '{}')".format(x_txt, self.emailAddy))

        # Put the contact details into each of the fields (this method
        # clears each field first).
        self._changeField('givenName', self.cont["givenName"])
        self._changeField('familyName', self.cont["familyName"])
        self._changeField('tel', self.cont["tel"]["value"])
        self._changeField('street', self.cont["addr"]["streetAddress"])
        self._changeField('zip', self.cont["addr"]["postalCode"])
        self._changeField('city', self.cont["addr"]["locality"])
        self._changeField('country', self.cont["addr"]["countryName"])

        # Add another email address.
        self.contacts.add_another_email_address(self.cont["email"]["value"])

        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()

        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@src,'contacts')]"),
                                              "Contact app iframe")

        # Now return to the SMS app.
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

    def _changeField(self, p_field, p_valObj):

        # To try and get around marionette issues I'm resetting Marionette every time here.

        self.UTILS.general.checkMarionetteOK()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        contFields = self.contacts.get_contact_fields()
        self.contacts.replace_str(contFields[p_field], p_valObj)
