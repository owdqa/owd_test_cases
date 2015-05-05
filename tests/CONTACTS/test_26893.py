from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit import DOM
from OWDTestToolkit.apps.contacts import Contacts


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        # Prepare the contact.
        self.contact = MockContact()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Launch contacts app.
        self.contacts.launch()
        self.contacts.start_create_new_contact()

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point", x)

        x = self.UTILS.element.getElement(DOM.Contacts.done_button, "Done button")
        self.UTILS.test.test(not x.is_enabled(), "Done button is not enabled")

        contFields = self.contacts.get_contact_fields()
        """
        Put the contact details into each of the fields (this method
        clears each field first).
        """

        self.contacts.replace_str(contFields['givenName'], self.contact["givenName"])
        self.contacts.replace_str(contFields['familyName'], self.contact["familyName"])

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point", x)

        x = self.UTILS.element.getElement(DOM.Contacts.done_button, "Done button")
        self.UTILS.test.test(x.is_enabled(), "Done button is not enabled")
        x.tap()

        self.contacts.view_contact(self.contact["name"])
