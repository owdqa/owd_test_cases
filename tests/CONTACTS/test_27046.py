#===============================================================================
# 27046: When the import finishes user is taken back to the contact
# list where it is possible to see the new contacts imported
#
# Pre-requisites:
# To have a gmail account with several contacts available to show/import
#
# Procedure:
# 1. Open Contacts app
# 2. Go to Settings
# 3. Tap on Import from Gmail
# 4. The log in screen is shown
# 5. Introduce a valid user/password
# 6. Tap on Sign In
# 7. Once the list of contacts is shown, select some of them
# 8. Then tap on Import
# 9. Verify user is taken to the addres book
#
# Expected results:
# User should be taken back to the contact list on the address book when
# the import finishes.
# All contacts imported are shown ok
#===============================================================================

from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.utils.contacts import MockContact


class test_main(PixiTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.gmail_user = self.UTILS.general.get_config_variable("gmail_1_user", "common")
        self.gmail_passwd = self.UTILS.general.get_config_variable("gmail_1_pass", "common")

        #
        # Create test contacts.
        #
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.connect_to_network()

        self.contacts.launch()
        self.contacts.import_gmail_login(self.gmail_user, self.gmail_passwd)
        self.num_gmail_contacts = len(self.marionette.find_elements(*DOM.Contacts.import_conts_list))

        #
        # Import them.
        #
        self.contacts.import_all()
        self.apps.kill_all()
        self.contacts.launch()

        #
        # Check all our contacts are in the list, both 'standard' ...
        #
        prepopulated_contact = (DOM.Contacts.view_all_contact_specific_contact[0],
                                DOM.Contacts.view_all_contact_specific_contact[1].format("OWD"))

        self.UTILS.element.waitForElements(prepopulated_contact, "Prepopulated Contact")

        # ... and the gmail contacts ...
        gmail_imported = (DOM.Contacts.view_all_contact_specific_contact[0],
                                DOM.Contacts.view_all_contact_specific_contact[1].format("roy"))
        contacts = self.UTILS.element.getElements(gmail_imported, "Gmail imported contacts")
        self.UTILS.test.test(len(contacts) == self.num_gmail_contacts, "All gmail contacts have been imported")