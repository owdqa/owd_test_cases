#===============================================================================
# 23887: Accept creating a new contact, editing some other fields
#
# Pre-requisites:
# Receive an SMS from a number which is not stored on the Address book
#
# Procedure:
# 1. Open the SMS
# 2. On the thread view tap on the header where the number is shown
# 3. Then tap on 'Create new' option
# 4. When the new contact screen is shown with the number filled in, edit name,
# surname and other fields, tap on Done
#
# Expected results:
# The contact should be created whit the changes done and user should be returned
# to the SMS thread view screen where the header is updated according to the
# contact added
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
import time


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()

        # View the contact details.
        self.contacts.view_contact(self.contact['name'])

        # Press the favourites button.
        fav_btn = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Favourite toggle button")
        fav_btn.tap()

        # Go back to view all contacts and check this contact is listed in the
        # 'favourites' section.
        back_btn = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Back button")
        back_btn.tap()

        # Check our test contact is listed in the group favourites.
        string = self.contact['givenName'] + self.contact['familyName']
        favs = ("xpath", DOM.Contacts.favourites_list_xpath.format(string.upper()))
        self.UTILS.element.waitForElements(favs, "'" + self.contact['name'] + "' in the favourites list")

        # View the contact.
        self.UTILS.reporting.logResult("info", "*** Removing contact as a favourite ... ***")
        self.contacts.view_contact(self.contact['name'])

        # Press the favourites button.
        fav_btn = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Favourite toggle button")
        self.UTILS.test.test(fav_btn.text == "Remove as Favorite",
                        "Favourite toggle button says 'Remove as Favorite' before contact is removed as a favorite.")
        fav_btn.tap()
        time.sleep(2)
        fav_btn = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Favourite toggle button")
        self.UTILS.test.test(fav_btn.text == "Add as Favorite",
                        "Favourite toggle button says 'Add as Favorite' after contact is removed as a favorite.")

        # Go back to view all contacts and check this contact is listed in the
        # 'favourites' section.
        back_btn = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Back button")
        back_btn.tap()

        # Check our test contact is no longer listed in the group favourites.
        string = self.contact['givenName'] + self.contact['familyName']
        favs = ("xpath", DOM.Contacts.favourites_list_xpath.format(string.upper()))
        self.UTILS.element.waitForNotElements(favs, "'" + self.contact['name'] + "' in the favourites list")
