# OWD-28542:  Verify that the user can cancel a importation from "SD CARD" while it's in process
#
# ** Procedure
#       1. Open contacts app
#       2. Press settings button
#       3. Select import form "SD CARD" option
#       4. Press import button
#       5. Press cancel button while the importation is in process
# ** Expected Results
#       The importation is canceled and any contact that have been imported during the cancelled import
#       session will not be removed. i.e. cancel is 'cancel' and not 'cancel and undo'
#
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.test_contact = MockContact()
        self.UTILS.general.insertContact(self.test_contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        contact_number = len(self.marionette.find_elements(*DOM.Contacts.view_all_contact_list))

        # Check the Memory Card button is enabled to begin with.
        self.contacts.import_memory_card()
        time.sleep(2)

        x = self.UTILS.element.getElement(DOM.Contacts.cancel_import_contacts, "Cancel the import")
        x.tap()
        time.sleep(2)

        # Check that the process has been actually cancelled, check the contact list??
        self.UTILS.element.waitForElements(DOM.Contacts.memorycard_button, "Memory Card Button")
