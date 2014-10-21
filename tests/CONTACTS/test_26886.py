from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Get details of our test contacts.
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
        # View the contact details.
        #
        self.contacts.view_contact(self.contact['name'])

        #
        # Press the favourites button.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Favourite toggle button")
        self.UTILS.test.TEST(x.text == "Add as Favorite",
                        "Favourite 'toggle' button is labelled 'Add as Favourite'.")
        x.tap()

        #
        # Verify the favourite toggle button label changes correctly.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Favourite toggle button")
        self.UTILS.test.TEST(x.text == "Remove as Favorite",
                        "Favourite 'toggle' button is labelled 'Remove as Favourite'.")

        #
        # Go back to view all contacts and check this contact is listed in the
        # 'favourites' section.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()

        string = self.contact['givenName'] + self.contact['familyName']
        favs = ("xpath", DOM.Contacts.favourites_list_xpath.format(string))
        self.UTILS.element.waitForElements(favs, "'" + self.contact['name'] + "' in the favourites list")
