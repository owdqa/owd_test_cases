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
        # Create test contacts.
        #
        self.contact_list = [MockContact(givenName=chr(65 + i) + "givenname", familyName=chr(67 - i) + "familyname")\
                             for i in range(3)]
        for i in range(3):
            self.contact_list[i]['name'] = "{} {}".format(self.contact_list[i]['givenName'],\
                                                          self.contact_list[i]['familyName'])
        map(self.UTILS.general.insertContact, self.contact_list)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Because we don't know what the initial state of the search order is, check it twice.
        #
        x = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        if x[0].text != self.contact_list[0]["name"]:
            self.UTILS.reporting.logResult("info", "(NOTE: it looks like the initial search order may need to be changed)")
            self.toggle_search_order()

        self.UTILS.reporting.logResult("info", "<b>Checking when sorted by given name (first name) ...</b>")
        x = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        self.UTILS.test.test(x[0].text == self.contact_list[0]["name"], "'{}' is the first contact listed.".\
                        format(self.contact_list[0]["name"]))
        self.UTILS.test.test(x[1].text == self.contact_list[1]["name"], "'{}' is the second contact listed.".\
                        format(self.contact_list[1]["name"]))
        self.UTILS.test.test(x[2].text == self.contact_list[2]["name"], "'{}' is the thrid contact listed.".\
                        format(self.contact_list[2]["name"]))

        self.toggle_search_order()

        self.UTILS.reporting.logResult("info", "<b>Checking when sorted by family name (last name) ...</b>")
        x = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        self.UTILS.test.test(x[0].text == self.contact_list[2]["name"], "'{}' is the first contact listed.".\
                        format(self.contact_list[2]["name"]))
        self.UTILS.test.test(x[1].text == self.contact_list[1]["name"], "'{}' is the second contact listed.".\
                        format(self.contact_list[1]["name"]))
        self.UTILS.test.test(x[2].text == self.contact_list[0]["name"], "'{}' is the third contact listed.".\
                        format(self.contact_list[0]["name"]))

    def toggle_search_order(self):
        self.UTILS.reporting.logResult("info", "<b>Changing sort order ...</b>")
        x = self.UTILS.element.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()
        x = self.UTILS.element.getElement(("id", "settingsOrder"), "'Order by last name' switch")
        x.tap()
        x = self.UTILS.element.getElement(DOM.Contacts.settings_done_button, "Done button")
        x.tap()
