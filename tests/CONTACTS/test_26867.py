from OWDTestToolkit.firec_testcase import FireCTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(FireCTestCase):

    num_contacts = 10

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Get details of our test contacts.
        #
        self.mock_contacts = [MockContact() for i in range(self.num_contacts)]

        map(self.UTILS.general.insertContact, self.mock_contacts)

        self.listContacts = [c["givenName"] for c in self.mock_contacts]

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
    
        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult('info', "Screenshot", screenshot)
        #
        # Verify list has 'num_contacts' contacts.
        #
        the_list = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        self.UTILS.test.test(self.num_contacts == len(the_list), "All contacts are showed")

        #
        # Verify contacts shown are the contact inserted.
        #
        count = 0
        for i in the_list:
            for c in self.listContacts:
                if (c in i.text):
                    self.UTILS.reporting.logResult("info", "Contact " + c + " inserted")
                    count += 1
                    break

        self.UTILS.test.test(count == self.num_contacts, "All contacts inserted")
