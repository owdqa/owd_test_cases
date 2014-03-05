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
        self.test_contacts = [MockContact() for i in range(2)]
        map(self.UTILS.insertContact, self.test_contacts)

        self.listNames = [c["givenName"] for c in self.test_contacts]
        self.listSurnames = [c["familyName"] for c in self.test_contacts]

        self.listNames.sort()

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Verify contacts shown are the contact inserted.
        #
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")

        for i in x:
            for j in range(len(self.listNames)):
                if self.listNames[j] in i.text and self.listSurnames[j] in i.text:
                    self.UTILS.logResult("info", "The contact shown {} has the name {}".\
                                         format(i.text, self.listNames[j]))
                    self.UTILS.logResult("info", "The contact shown {} has the surname {}".\
                                         format(i.text, self.listSurnames[j]))
