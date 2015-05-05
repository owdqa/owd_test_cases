from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
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

        # Check the Import button is disabled to begin with.
        x = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.test(x.get_attribute("disabled") == "true", "Import button is disabled.")
        """
        Select / de-select contacts and make sure Import button is enabled / disabled
        as expected.
        """

        self.UTILS.reporting.logResult("info", "Enable contact 1...")
        self.contacts.import_toggle_select_contact(1)

        x = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.test(x.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.reporting.logResult("info", "Enable contact 2...")
        self.contacts.import_toggle_select_contact(2)

        x = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.test(x.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.reporting.logResult("info", "Disable contact 2...")
        self.contacts.import_toggle_select_contact(2)

        x = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.test(x.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.reporting.logResult("info", "Disable contact 1...")
        self.contacts.import_toggle_select_contact(1)

        x = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.test(x.get_attribute("disabled") == "true", "Import button is disabled.")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", x)
