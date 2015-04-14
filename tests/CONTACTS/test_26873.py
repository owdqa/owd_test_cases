from OWDTestToolkit.firec_testcase import FireCTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(FireCTestCase):

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
        self.contact = MockContact()

        self.nameIncomplete = self.contact["givenName"][:4]
        self.surnameIncomplete = self.contact["familyName"][:2]

        name2 = self.nameIncomplete + "h"
        fname2 = self.surnameIncomplete + "t"

        self.contact2 = MockContact(givenName=name2, familyName=fname2)
        self.contact3 = MockContact(givenName='John', familyName='Smith')

        self.UTILS.general.insertContact(self.contact)
        self.UTILS.general.insertContact(self.contact2)
        self.UTILS.general.insertContact(self.contact3)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # With nameIncomplete : Search for the sought contact.
        #
        self.contacts.search(self.nameIncomplete)

        #
        # With nameIncomplete: Verify our contact is listed.
        #
        self.contacts.check_search_results(self.contact["givenName"])
        self.contacts.check_search_results(self.contact2["givenName"])

        #
        # With nameIncomplete: Verify the other contact is NOT listed.
        #
        self.contacts.check_search_results(self.contact3["givenName"], False)

        #
        # Enter one more letter.
        #
        self.UTILS.general.typeThis(DOM.Contacts.search_contact_input, "Search input", self.nameIncomplete + self.contact["givenName"][4],
                            p_no_keyboard=True, p_validate=False, p_clear=False, p_enter=False)

        #
        # Verify list updated.
        #
        self.contacts.check_search_results(self.contact["givenName"])
        self.contacts.check_search_results(self.contact2["givenName"], False)
        self.contacts.check_search_results(self.contact3["givenName"], False)

        #
        # Cancel search.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.search_cancel_btn, "Search cancel button")
        x.tap()

        #
        # With surnameIncomplete : Search for the sought contact.
        #
        self.contacts.search(self.surnameIncomplete)

        #
        # With surnameIncomplete: Verify our contact is listed.
        #
        self.contacts.check_search_results(self.contact["familyName"])
        self.contacts.check_search_results(self.contact2["familyName"])

        #
        # With surnameIncomplete: Verify the other contact is NOT listed.
        #
        self.contacts.check_search_results(self.contact3["familyName"], False)

        #
        # Enter one more letter.
        #
        self.UTILS.general.typeThis(DOM.Contacts.search_contact_input, "Search input", self.surnameIncomplete + self.contact["familyName"][2],
                            p_no_keyboard=True, p_validate=False, p_clear=False, p_enter=False)

        #
        # Verify list updated.
        #
        self.contacts.check_search_results(self.contact["familyName"])
        self.contacts.check_search_results(self.contact2["familyName"], False)
        self.contacts.check_search_results(self.contact3["familyName"], False)
