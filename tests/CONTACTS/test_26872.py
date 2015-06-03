from gaiatest import GaiaTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        # Get details of our test contacts.
        self.test_contacts = [MockContact() for i in range(3)]
        self.test_contacts[0]["givenName"] = "Johnname"
        self.test_contacts[0]["familyName"] = "Smname" 

        self.endWord = "name"

        map(self.UTILS.general.insertContact, self.test_contacts)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Launch contacts app.
        self.contacts.launch()

        # With name: Search for the sought contact.
        self.contacts.search(self.endWord)

        # With name: Verify our contact is listed.
        self.contacts.check_search_results(self.test_contacts[0]["givenName"])

        # With name: Verify the other contact is NOT listed.
        self.contacts.check_search_results(self.test_contacts[1]["givenName"], False)
        self.contacts.check_search_results(self.test_contacts[2]["givenName"], False)
