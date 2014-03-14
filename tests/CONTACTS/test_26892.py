#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContact
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
import time


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Prepare the contact.
        #
        self.contact = MockContact()
        self.UTILS.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):

        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # View the details of our contact and make him a favourite.
        #
        self.UTILS.logResult("info", "<b>Setting up a contact in favourites ...</b>")
        self.contacts.view_contact(self.contact['name'])

        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        x.tap()

        x = self.UTILS.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()

        self.UTILS.waitForElements(DOM.Contacts.favourites_section, "Favourites section")

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point", x)

        self.UTILS.logResult("info", "<b>removing contact from favourites ...</b>")
        self.contacts.view_contact(self.contact['name'])

        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        x.tap()

        x = self.UTILS.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()

        time.sleep(1)
        self.UTILS.waitForNotElements( DOM.Contacts.favourites_section, "Favourites section")

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point", x)
