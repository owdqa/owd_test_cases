#===============================================================================
# 26887: Remove a contact from the favorites list
#
# Procedure:
# 1- Open Address book
# 2- Select a contact and enter in contact details
# 3- Remove the contact from the favorites list
#
# Expected results:
# The contact is removed from the list
# Favourite button changes from active to inactive state.
#===============================================================================

from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
import time


class test_main(PixiTestCase):

    add_fav_str = "Add as Favorite"
    remove_fav_str = "Remove as Favorite"

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Prepare the contact.
        #
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # View the details of our contact and make him a favourite.
        #
        self.UTILS.reporting.logResult("info", "<b>Setting up a contact in favourites ...</b>")
        self.contacts.view_contact(self.contact['name'])

        fav_btn = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        self.UTILS.test.test(fav_btn.text == self.add_fav_str, "Toggle favourite button text is '{}'.".\
                        format(self.add_fav_str))
        fav_btn.tap()
        fav_btn = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (after tap)")
        self.UTILS.test.test(fav_btn.text == self.remove_fav_str, "Toggle favourite button text is '{}'.".\
                        format(self.remove_fav_str))

        back_btn = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Back button")
        back_btn.tap()

        string = self.contact['givenName'] + self.contact['familyName']
        favs = ("xpath", DOM.Contacts.favourites_list_xpath.format(string.upper()))
        self.UTILS.element.waitForElements(favs, "'" + self.contact['name'] + "' in the favourites list")

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point", screenshot)

        self.UTILS.reporting.logResult("info", "<b>removing contact from favourites ...</b>")
        self.contacts.view_contact(self.contact['name'])

        fav_btn = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        self.UTILS.test.test(fav_btn.text == self.remove_fav_str, "Toggle favourite button text is '{}'.".\
                        format(self.remove_fav_str))
        fav_btn.tap()
        fav_btn = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (after tap)")
        self.UTILS.test.test(fav_btn.text == self.add_fav_str, "Toggle favourite button text is '{}'.".\
                        format(self.add_fav_str))

        back_btn = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Back button")
        back_btn.tap()

        time.sleep(1)
        string = self.contact['givenName'] + " " + self.contact['familyName']
        favs = ("xpath", DOM.Contacts.favourites_list_xpath.format(string.upper()))
        self.UTILS.element.waitForNotElements(favs, "'" + self.contact['name'] + "' in the favourites list")

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point", screenshot)
