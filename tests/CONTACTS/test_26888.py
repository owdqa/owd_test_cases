#===============================================================================
# 26888: Verify that the favourite contacts will be listed on the top of the full
# contact list
#
# Procedure:
# 1- Open Address book app
# 2- Navigate to the top of contacts lists.
#
# Expected results:
# The favourite contacts are listed on the top of the full contact list and in
# letter position.
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        # Prepare the contacts.
        self.contact_list = [MockContact() for i in range(3)]
        map(self.UTILS.general.insertContact, self.contact_list)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()

        # View the details of our contact and make him a favourite.
        self.UTILS.reporting.logResult("info", "<b>Setting up a contact in favourites ...</b>")
        self.contacts.view_contact(self.contact_list[0]['name'])

        # Mark contact as favourite
        fav_btn = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        fav_btn.tap()

        #
        # Go back to all contacts list
        #
        back_btn = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Back button")
        back_btn.tap()

        #
        # Check the contact is in the favourite list
        #
        string = self.contact_list[0]['givenName'] + self.contact_list[0]['familyName']
        favs = ("xpath", DOM.Contacts.favourites_list_xpath.format(string.upper()))
        self.UTILS.element.waitForElements(favs, "'" + self.contact_list[0]['name'] + "' in the favourites list")

        # Now check the favourites list appears first.
        fav_list = self.UTILS.element.getElements(("tag name", "ol"), "Contact lists")
        fav_id = "contacts-list-favorites"
        normal_ids = "contacts-list-"

        foundFav = False
        foundNormal = False
        for i in fav_list:
            if fav_id in i.get_attribute("id"):
                foundFav = True
            if normal_ids in i.get_attribute("id"):
                foundNormal = True
                break

        self.UTILS.test.test(foundNormal, "Found the non-favourite lists.")
        self.UTILS.test.test(foundFav, "Found the favourite lists before the non-favourite lists.")
