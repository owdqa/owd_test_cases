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
        self.contact_list = [MockContact() for i in range(3)]
        map(self.UTILS.general.insertContact, self.contact_list)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Launch contacts app.
        self.contacts.launch()

        # Search for our new contact.
        self.contacts.search(self.contact_list[0]["tel"]["value"])

        # Verify that we're now in the 'search results' screen.
        self.UTILS.element.waitForElements(DOM.Contacts.search_results_list, "Search results list")

        # Cancel the search.
        x = self.UTILS.element.getElement(DOM.Contacts.search_cancel_btn, "Cancel search button")
        x.tap()

        # Verify that we're no longer in the 'search results' screen.
        self.UTILS.element.waitForNotElements(DOM.Contacts.search_results_list, "Search results list")
