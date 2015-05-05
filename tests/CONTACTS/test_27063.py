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

        # Get details of our test contacts.
        self.contact = MockContact(givenName='1111111')
        self.contact2 = MockContact(familyName='2222222')

        self.UTILS.general.insertContact(self.contact)
        self.UTILS.general.insertContact(self.contact2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Launch contacts app.
        self.contacts.launch()

        # Search for our new contact.
        self.UTILS.reporting.logResult("info", "<b>Search against number in 'given name' field ...</b>")
        self.contacts.search('1111111')
        self.contacts.check_search_results(self.contact["givenName"])

        x = self.UTILS.element.getElement(DOM.Contacts.search_cancel_btn, "Search cancel button")
        x.tap()

        self.UTILS.reporting.logResult("info", "<b>Search against number in 'family name' field ...</b>")
        self.contacts.search('2222222')
        self.contacts.check_search_results(self.contact2["familyName"])
