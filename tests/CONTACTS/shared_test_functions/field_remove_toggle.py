#
# Runs through composing and sending an email as one user, then
# receiving it as another user.
#
# As I can't see ANY different between read and unread emails in the html,
# I need to rely on a totally unique subject line to identify the precise
# message sent between the two test accounts.
#

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts


class field_remove_toggle(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

    def tearDown(self):
        self.UTILS.general.remove_files()
        self.UTILS.reporting.reportResults()

    def field_remove_toggle_test(self, contact, field_definition, item_nums=[0]):
        """
        Imports a contact, goes to the contact, edits it and tests the required 'remove' icon
        (on and then off).
        p_field_num: The number of the item, for example if there's >1 phone number, then '0' would
        be the first one etc... (defaults to zero in case there's only one item).
        """

        del_icon_locator = ("css selector", DOM.Contacts.reset_field_css.format(field_definition))

        if field_definition == "thumbnail-action":

            # The thumbnail is different from the rest.
            field_locator = DOM.Contacts.edit_image
        else:
            field_locator = ("xpath", "//div[@id='{}']/div".format(field_definition))

        # Get details of our test contacts.
        self.UTILS.reporting.logResult("info", "Setting up contact ...")
        self.UTILS.general.insertContact(contact)

        # Add image.
        self.UTILS.general.add_file_to_device('./tests/_resources/contact_face.jpg')
        self.contacts.launch()
        self.contacts.view_contact(contact['name'])
        self.contacts.press_edit_contact_button()
        self.contacts.add_gallery_image_to_contact(0)

        self.UTILS.reporting.logResult("info", "Starting tests ...")

        # Try to make sure this field section is in view (pretty hideous, but it does the job!).
        try:
            self.marionette.execute_script("document.getElementById('{}').scrollIntoView();".format(field_definition))
            self.marionette.execute_script("document.getElementById('contact-form-title').scrollIntoView();")
        except:
            pass

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point:", x)

        self.UTILS.general.checkMarionetteOK()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        self.UTILS.reporting.logResult("info", "<b>For each of our items for this field, "\
                             "click the icon to set them to 'remove' ...</b>")
        for i in item_nums:
            x = self.UTILS.element.getElements(field_locator, "Field being tested (item {})".format(i))[i]
            self.UTILS.test.test("removed" not in x.get_attribute("class"),
                            "The item is NOT marked as temporarily removed.")

            x = self.UTILS.element.getElements(del_icon_locator, "Field reset button (item {})".format(i))[i]
            x.tap()

            x = self.UTILS.debug.screenShotOnErr()
            self.UTILS.reporting.logResult("info", "Screenshot at this point:", x)

            x = self.UTILS.element.getElements(field_locator, "Field being tested (item {})".format(i))[i]
            self.UTILS.test.test("removed" in x.get_attribute("class"), "The item IS now marked as temporarily removed.")

        self.UTILS.reporting.logResult("info", "<b>For each of our items for this field, "\
                             "click the icon to turn off 'remove' ...</b>")
        for i in item_nums:
            x = self.UTILS.element.getElements(del_icon_locator, "Field reset button (item {})".format(i))[i]
            x.tap()

            x = self.UTILS.debug.screenShotOnErr()
            self.UTILS.reporting.logResult("info", "Screenshot at this point:", x)

            x = self.UTILS.element.getElements(field_locator, "Field being tested (item {})".format(i))[i]
            self.UTILS.test.test("removed" not in x.get_attribute("class"),
                            "The item is now NOT marked as temporarily removed.")
