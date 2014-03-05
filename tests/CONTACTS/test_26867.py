#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    num_contacts = 10

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
        self.mock_contacts = [MockContact() for i in range(self.num_contacts)]

        map(self.UTILS.insertContact, self.mock_contacts)

        self.listContacts = [c["givenName"] for c in self.mock_contacts]

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Verify list has 'num_contacts' contacts.
        #
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        self.UTILS.TEST(self.num_contacts == len(x), "All contacts are showed")

        #
        # Verify contacts shown are the contact inserted.
        #
        count = 0
        for i in x:
            for c in self.listContacts:
                if (c in i.text):
                    self.UTILS.logResult("info", "Contact " + c + " inserted")
                    count += 1
                    break

        self.UTILS.TEST(count == self.num_contacts, "All contacts inserted")
