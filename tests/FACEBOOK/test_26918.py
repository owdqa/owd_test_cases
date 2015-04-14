# OWD-26918
# Unlink all Facebook contacts in the address book in a single step and
# verify the contacts who was linked to a facebook contacts

# ** Procedure
#       1. Create a Contact With The name "Test"
#       2. Link contact with a contact in Facebook
#       3. Open settings contact list
#       4. Press the toggle to delete all facebook contacts
#       5. Press Remove
#   
# ** Expected Results
# FB contacts are deleted. If a contact was linked to one of Facebook. 
# The contact is displayed as if you had unlinked

from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.facebook import Facebook
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.utils.contacts import MockContact


class test_main(FireCTestCase):

    def setUp(self):

        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.facebook = Facebook(self)

        self.fb_user = self.UTILS.general.get_config_variable("gmail_1_email", "common")
        self.fb_pass = self.UTILS.general.get_config_variable("gmail_1_pass", "common")
        self.fb_email = self.UTILS.general.get_config_variable("gmail_2_email", "common")

        self.test_contact = MockContact()
        self.UTILS.general.insertContact(self.test_contact)

        self.data_layer.connect_to_wifi()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):

        self.contacts.launch()
        self.contacts.tapSettingsButton()
        self.contacts.enable_FB_import()
        self.facebook.login(self.fb_user, self.fb_pass)

        # Import all
        self.contacts.switch_to_facebook()
        self.facebook.importAll()

        # Go back to "All contacts" screen
        back_btn = self.UTILS.element.getElement(DOM.Contacts.settings_done_button, "Details 'done' button")
        back_btn.tap()

        # View the contact details.
        self.contacts.view_contact(self.test_contact['name'])

        # Press the link button.
        self.contacts.tapLinkContact()

        # Select the contact to link.
        self.facebook.link_contact(self.fb_email)

        # Check we're back at our contact.
        self.UTILS.element.headerCheck(self.test_contact['name'])

        # Verify that we're now linked.
        self.contacts.verify_linked(self.test_contact['name'], self.fb_email)
