from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
import time
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.gmail_user = self.UTILS.general.get_config_variable("gmail_1_user", "common")
        self.gmail_passwd = self.UTILS.general.get_config_variable("gmail_1_pass", "common")

        self.connect_to_network()
        # Create test contacts.
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        self.contacts.import_gmail_login(self.gmail_user, self.gmail_passwd)

        # Check the Import button is disabled to begin with.
        x = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.test(x.get_attribute("disabled") == "true", "Import button is disabled.")

        # Tap the Select All button (can't be done with marionette yet).
        self.UTILS.element.waitForElements(DOM.Contacts.import_select_all, "Select_all button")
        self.UTILS.reporting.logResult("info", "Tapping the 'Select All' button ...")
        self.marionette.execute_script("document.getElementById('{}').click()".\
                                       format(DOM.Contacts.import_select_all[1]))
        time.sleep(1)

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", x)

        x = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.test(x.get_attribute("disabled") != "true", "Import button is enabled.")

        """
        The only way I can see to test that all contacts are selected is to toggle
        all of them and make sure the Import button is then disabled (because that
        means all of them were selected before the toggle).
        """
        x = self.UTILS.element.getElements(("class name", "block-item"), "Contacts list")
        for i in range(len(x)):
            i_num = i + 1
            self.UTILS.reporting.logResult("info", "Disable contact {} ...".format(i_num))
            self.contacts.import_toggle_select_contact(i_num)

        x = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.test(x.get_attribute("disabled") == "true", "Import button is disabled.")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", x)
