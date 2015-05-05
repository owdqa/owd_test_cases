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

        # Create test contacts.
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        self.contacts.view_contact(self.contact['name'])
        self.contacts.press_edit_contact_button()

        self.marionette.execute_script("document.getElementById('delete-contact').scrollIntoView();")
        self.marionette.execute_script("document.getElementById('contact-form-title').scrollIntoView();")

        x = self.UTILS.element.getElement(DOM.Contacts.delete_contact_btn, "Delete contact button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Contacts.confirm_delete_btn, "Confirmation button")
        y = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point:", y)
        x.tap()

        self.UTILS.element.waitForElements(("xpath", "//p[text()='No contacts']"), "'No contacts' message")
        y = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point:", y)
