#===============================================================================
# 26901: Search a contact after edit contact name
#
# Procedure:
# 1- Open contact app
# 2- Select a contact
# 3- Edit contact nane, changing the actual name for a very long name "aaaaabbbbbccccaaaa"
# 4- Press Done button
# 5- Press over search field
# 6- Type aaa
# 7- Tap in the contact shown
#
# Expected result:
# Contact detail is opened
#===============================================================================

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        # Create test contacts.
        self.test_contacts = [MockContact() for i in range(2)]
        map(self.UTILS.general.insertContact, self.test_contacts)
        self.new_given_name = "aaaaabbbbbccccaaaa"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Set up to use data connection.
        self.connect_to_network()

        # Launch contacts app.
        self.contacts.launch()

        # Change the name to "aaaaabbbbbccccaaaa"
        self.contacts.change_contact(self.test_contacts[0]['name'], "givenName",
                                    self.new_given_name)

        # Search for our new contact.
        self.contacts.search("aaa")

        # Verify our contact is listed.
        self.contacts.check_search_results(self.new_given_name, True)

        # Verify the other contact is NOT listed.
        self.contacts.check_search_results(self.test_contacts[1]["givenName"], False)
