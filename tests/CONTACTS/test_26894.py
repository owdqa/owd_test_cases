from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        self.contact = MockContact()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        self.contacts.start_create_new_contact()

        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "Done button")
        self.UTILS.test.test(not done_button.is_enabled(), "Done button is not enabled")

        contFields = self.contacts.get_contact_fields()

        """
        Put the contact details into each of the fields (this method
        clears each field first).
        """
        self.contacts.replace_str(contFields['tel'], self.contact["tel"]["value"])

        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "Done button")
        self.UTILS.test.test(done_button.is_enabled(), "Done button is not enabled")
        done_button.tap()

        self.contacts.view_contact(self.contact["tel"]["value"])
