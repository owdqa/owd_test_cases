#===============================================================================
# 26886: Configure a contact as a favourite
#
# Procedure:
# 1- Open Address book
# 2- Select a contact and enter in contact edit mode
# 3- Press add as favourite button
#
# Expected results:
# The contact is added to favorites list
# Favourite button changes from add to remove as favourite.
#===============================================================================


from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()

        # View the contact details.
        self.contacts.view_contact(self.contact['name'])

        # Press the favourites button.
        fav_btn = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Favourite toggle button")
        self.UTILS.test.test(fav_btn.text == "Add as Favorite",
                        "Favourite 'toggle' button is labelled 'Add as Favourite'.")
        fav_btn.tap()

        # Verify the favourite toggle button label changes correctly.
        fav_btn = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Favourite toggle button")
        self.UTILS.test.test(fav_btn.text == "Remove as Favorite",
                        "Favourite 'toggle' button is labelled 'Remove as Favourite'.")

        # Go back to view all contacts and check this contact is listed in the
        # 'favourites' section.
        self.contacts.go_back_from_contact_details()

        string = self.contact['givenName'] + self.contact['familyName']
        favs = ("xpath", DOM.Contacts.favourites_list_xpath.format(string.upper()))
        self.UTILS.element.waitForElements(favs, "'" + self.contact['name'] + "' in the favourites list")
