from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        # Create our test contacts.
        self.contact_list = [MockContact(tel={'type': 'Mobile', 'value': "{}".format(i) * 9}) for i in range(3)]
        map(self.UTILS.general.insertContact, self.contact_list)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Launch contacts app.
        self.contacts.launch()

        # Search for our new contact.
        self.contacts.search("999999999")

        # Verify that there are no results.
        self.UTILS.element.waitForElements(DOM.Contacts.search_no_contacts_found, "'No contacts found' message")
