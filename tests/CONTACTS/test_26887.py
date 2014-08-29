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
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
import time


class test_main(GaiaTestCase):

    add_fav_str = "Add as Favorite"
    remove_fav_str = "Remove as Favorite"

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
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

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

        x = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        self.UTILS.test.TEST(x.text == self.add_fav_str, "Toggle favourite button text is '{}'.".\
                        format(self.add_fav_str))
        x.tap()
        x = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (after tap)")
        self.UTILS.test.TEST(x.text == self.remove_fav_str, "Toggle favourite button text is '{}'.".\
                        format(self.remove_fav_str))

        x = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()

        string = self.contact['givenName'] + self.contact['familyName']
        favs = ("xpath", DOM.Contacts.favourites_list_xpath.format(string))
        self.UTILS.element.waitForElements(favs, "'" + self.contact['name'] + "' in the favourites list")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point", x)

        self.UTILS.reporting.logResult("info", "<b>removing contact from favourites ...</b>")
        self.contacts.view_contact(self.contact['name'])

        x = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        self.UTILS.test.TEST(x.text == self.remove_fav_str, "Toggle favourite button text is '{}'.".\
                        format(self.remove_fav_str))
        x.tap()
        x = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (after tap)")
        self.UTILS.test.TEST(x.text == self.add_fav_str, "Toggle favourite button text is '{}'.".\
                        format(self.add_fav_str))

        x = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()

        time.sleep(1)
        string = self.contact['givenName'] + " " + self.contact['familyName']
        favs = ("xpath", DOM.Contacts.favourites_list_xpath.format(string))
        self.UTILS.element.waitForNotElements(favs, "'" + self.contact['name'] + "' in the favourites list")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point", x)
