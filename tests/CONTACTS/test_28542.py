from OWDTestToolkit.firec_testcase import FireCTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
import time

class test_main(FireCTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.contacts.launch()

        #
        # Check the Memory Card button is enabled to begin with.
        #
        self.contacts.import_memory_card()
        time.sleep(2)

        x = self.UTILS.element.getElement(DOM.Contacts.cancel_import_contacts, "Cancel the import")
        x.tap()
        time.sleep(2)

        #Check that the process has been actually cancelled, check the contact list??
        self.UTILS.element.waitForElements(DOM.Contacts.memorycard_button, "Memory Card Button")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", x)
