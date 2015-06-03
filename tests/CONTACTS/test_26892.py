from gaiatest import GaiaTestCase

from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
import time


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        # Prepare the contact.
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def toggle_fav(self, contact_name):
        self.contacts.view_contact(contact_name)
        fav_btn = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        fav_btn.tap()
        self.contacts.go_back_from_contact_details()

    def test_run(self):
        self.contacts.launch()

        # View the details of our contact and make him a favourite.
        self.UTILS.reporting.logResult("info", "<b>Setting up a contact in favourites ...</b>")
        self.toggle_fav(self.contact["name"])
        self.UTILS.element.waitForElements(DOM.Contacts.favourites_section, "Favourites section")

        self.UTILS.reporting.logResult("info", "<b>Removing contact from favourites ...</b>")
        self.toggle_fav(self.contact['name'])
        self.UTILS.element.waitForNotElements(DOM.Contacts.favourites_section, "Favourites section")
