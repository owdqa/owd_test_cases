#===============================================================================
# 26907: Remove a photo,a phone number, an email, an address and a
# comment from a contact and restore the phone number and the comment
#
# Procedure:
# 1- Open contact app
# 2- Select a contact with all fields filled
# 3- Open contact details
# 4- Press edit button
# 5- Remove contact photo
# 6- Remove contact phone number
# 7- Remove contact email
# 8- Remove contact address
# 9- Remove contact comment
# ER1
# 10- Press restore phone number
# 11- Press restore comment
# ER2
#
# Expected results:
# ER1: All deleted fields appear marked as "temporarily removed" with a
# dark shadow and an icon that will allow to restore it for each deleted field
# ER2: Phone number and comment fields are restored
#===============================================================================

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact
from marionette.by import By


class test_main(GaiaTestCase):

    _keyboard_frame_locator = (By.CSS_SELECTOR, '#keyboards iframe:not([hidden])')

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Create test contacts.
        #
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)
        self.UTILS.general.add_file_to_device('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.UTILS.reporting.logResult("info", "Setting up contact ...")
        self.contacts.launch()

        #
        # View our contact.
        #
        self.contacts.view_contact(self.contact['name'])

        #
        # Edit our contact.
        #
        self.contacts.press_edit_contact_button()

        self.UTILS.reporting.logResult("info", "Starting tests ...")

        self.check_field(True, "phone", "number_0", "number")
        self.check_field(True, "email", "email_0", "email")
        self.check_field(True, "address", "streetAddress_0", "streetAddress")

        # NOTE: for some reason the photo has to tested alone or it screws up the text tests.
        self.contacts.press_cancel_edit_button()
        self.contacts.press_edit_contact_button()
        self.contacts.add_gallery_image_to_contact(0)
        self.check_field(False, "photo", "thumbnail-action")

    def check_field(self, text, field_name, field_id, reset_btn_name=""):
        #
        # Test a text field: default, with reset enabled, with reset disabled.
        #

        #
        # try to make sure the field is in view (pretty hideous, but it does the job!).
        #
        try:
            self.marionette.execute_script("document.getElementById('" + field_id + "').scrollIntoView();")
            self.marionette.execute_script("document.getElementById('contact-form-title').scrollIntoView();")
        except:
            pass

        self.UTILS.reporting.logResult("info", " ")
        self.UTILS.reporting.logResult("info", "*** '" + field_name + "': default (before testing 'reset' mode) ... ***")
        self.check_kbd_appears(reset_btn_name, field_name, True) if text else self.check_photo_tap(True)

        self.UTILS.reporting.logResult("info", " ")
        self.UTILS.reporting.logResult("info", "*** '" + field_name + "': switching 'reset' mode ON ... ***")
        self.toggle_reset_button(field_name)
        self.check_kbd_appears(reset_btn_name, field_name, False) if text else self.check_photo_tap(False)

        self.UTILS.reporting.logResult("info", " ")
        self.UTILS.reporting.logResult("info", "*** '" + field_name + "': switching 'reset' mode OFF ... ***")
        self.toggle_reset_button(field_name)
        self.check_kbd_appears(reset_btn_name, field_name, True) if text else self.check_photo_tap(True)

        self.UTILS.reporting.logResult("info", " ")

    def toggle_reset_button(self, element):
        #
        # Press reset button on the required fields ...
        #
        reset_btn = DOM.Contacts.reset_field_xpath

        if element == "photo":
            x = self.UTILS.element.getElement(("xpath", reset_btn.format("thumbnail-action")), "Photo reset button")
            x.tap()

        if element == "phone":
            x = self.UTILS.element.getElement(("xpath", reset_btn.format("add-phone-0")), "Phone reset button")
            x.tap()

        if element == "email":
            x = self.UTILS.element.getElement(("xpath", reset_btn.format("add-email-0")), "Email reset button")
            x.tap()

        if element == "address":
            x = self.UTILS.element.getElement(("xpath", reset_btn.format("add-address-0")), "Address reset button")
            x.tap()

    def check_photo_tap(self, editable):
        time.sleep(1)

        # Check tapping photo (same link for add and edit)
        _comment = "Photo is " + ("not " if not editable else "")
        x = self.UTILS.element.getElement(DOM.Contacts.add_photo, "Photo")
        x.tap()
        time.sleep(1)

        self.marionette.switch_to_frame()

        is_editable = False
        try:
            self.wait_for_element_present(*DOM.Contacts.photo_from_gallery, timeout=5)
            self.wait_for_element_present(*DOM.Contacts.cancel_photo_source, timeout=1)
            x = self.marionette.find_element(*DOM.Contacts.cancel_photo_source)
            x.tap()
            is_editable = True
        except:
            is_editable = False
        self.UTILS.test.test(is_editable == editable, _comment + "editable.")
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

    def check_kbd_appears(self, item, desc, kbd_displayed):
        time.sleep(1)
        #
        # Taps the field and checks to see if the keyboard appears.
        # When marionette "is_enabled()" is working , we can forget all this.
        #
        comment = "The " + desc + " field can" + ("not" if not kbd_displayed else "") + " be edited."

        x = self.UTILS.element.getElement(("id", "{}_0".format(item)), "Field for " + desc)

        # From here on does the keyboard verification.
        # The problem is that the keyboard frame is always present
        # once it's been launched, so I need a way to either KILL
        # the keyboard, or see what's currently displayed.
        x.tap()

        self.marionette.switch_to_frame()
        kbd = False
        try:
            self.wait_for_element_displayed(*self._keyboard_frame_locator)
            screenshot = self.UTILS.debug.screenShotOnErr()
            self.UTILS.reporting.logResult('info', "Keyboard displayed", screenshot)
            kbd = True
        except:
            self.UTILS.reporting.logResult("info", "No wild keyboard appeared")
            # pass
            # 
        self.UTILS.reporting.logResult("info", "Is keyboard really there? {}".format(kbd))
        self.UTILS.reporting.logResult("info", "Expected: {}".format(kbd_displayed))

        self.UTILS.test.test(kbd == kbd_displayed, comment)

        #
        # Return to the contacts iframe.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        #
        # Tap the header to remove the keyboard.
        #
        self.wait_for_element_displayed(*DOM.Contacts.edit_contact_header)
        x = self.marionette.find_element(*DOM.Contacts.edit_contact_header)
        x.tap()
