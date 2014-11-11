# OWD-35086: Verify that is possible to select a contact which is marked as favorite
import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.contacts import MockContact


class main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)
        self.fxa_user = self.UTILS.general.get_os_variable("GLOBAL_FXA_USER")
        self.fxa_pass = self.UTILS.general.get_os_variable("GLOBAL_FXA_PASS")

        self.target_name = "QA"
        self.test_contacts = [MockContact() for i in range(3)]
        self.test_contacts[0]["givenName"] = self.target_name
        self.test_contacts[0]["familyName"] = "Automation"
        self.test_contacts[0]["name"] = "{} {}".format(
            self.test_contacts[0]["givenName"], self.test_contacts[0]["familyName"])
        map(self.UTILS.general.insertContact, self.test_contacts)
    
        self.contacts.launch()
        self._add_contact_as_favorite(self.test_contacts[0])

        self.connect_to_network()
        self.loop.initial_test_checks()
        self.settings.launch()
        self.settings.fxa()
        self.settings.fxa_log_out()
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # First, login
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.firefox_login(self.fxa_user, self.fxa_pass)
            self.loop.allow_permission_ffox_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")

            self.loop.open_address_book()
            elem = (DOM.Contacts.view_all_contact_specific_contact[
                    0], DOM.Contacts.view_all_contact_specific_contact[1].format(self.test_contacts[0]["givenName"]))
            self.UTILS.element.waitForElements(elem, "Contact in address book")

    def _add_contact_as_favorite(self, contact):
        self.contacts.view_contact(contact['name'])

        favorite_btn = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Favourite toggle button")
        favorite_btn.tap()

        back_btn = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Back button")
        back_btn.tap()

        string = "{}{}".format(contact['givenName'], contact['familyName']).upper()
        favs = ("xpath", DOM.Contacts.favourites_list_xpath.format(string))
        self.UTILS.element.waitForElements(favs, "'" + contact['name'] + "' in the favourites list")
