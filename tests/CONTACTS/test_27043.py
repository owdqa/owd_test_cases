from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
import time
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.gmail_user = self.UTILS.general.get_config_variable("gmail_1_user", "common")
        self.gmail_passwd = self.UTILS.general.get_config_variable("gmail_1_pass", "common")

        # Create test contacts.
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Set up to use data connection.
        self.connect_to_network()

        self.contacts.launch()
        self.contacts.import_gmail_login(self.gmail_user, self.gmail_passwd)

        self.contacts.import_toggle_select_contact(1)

        self.marionette.execute_script("document.getElementById('{}').click()".format(DOM.Contacts.import_import_btn[1]))
        time.sleep(1)

        self.apps.kill_all()
        time.sleep(2)
        self.contacts.launch()

        # Check our two contacts are in the list.
        prepopulated_contact = (DOM.Contacts.view_all_contact_specific_contact[0],
                                DOM.Contacts.view_all_contact_specific_contact[1].format("OWD"))

        self.UTILS.element.waitForElements(prepopulated_contact, "Prepopulated Contact")

        gmail_imported = (DOM.Contacts.view_all_contact_specific_contact[0],
                                DOM.Contacts.view_all_contact_specific_contact[1].format("roy"))

        self.UTILS.element.waitForElements(gmail_imported, "Gmail imported contact")

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", screenshot)
