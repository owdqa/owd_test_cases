from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        self.Contact_1 = MockContact()
        self.num = self.UTILS.general.get_config_variable("phone_number", "custom")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Enter a number in the dialer.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)

        #
        # Press the add to contacts button, then select 'add to existing contact'.
        #
        x = self.UTILS.element.getElement(DOM.Dialer.add_to_contacts_button, "Add to contacts button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Dialer.create_new_contact_btn, "Create new contact button")
        x.tap()

        #
        # Enter the details of the new contact.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        contFields = self.contacts.get_contact_fields()
        self.contacts.replace_str(contFields['givenName'], self.Contact_1["givenName"])
        self.contacts.replace_str(contFields['familyName'], self.Contact_1["familyName"])

        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()

        #
        # Verify that the contacts app is closed and we are returned to the call log.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@{}, '{}')]".\
                                               format(DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                              "Contacts frame")
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

        #
        # Verify that this contact has been created in contacts.
        #
        self.apps.kill_all()
        self.contacts.launch()
        self.contacts.view_contact(self.Contact_1["name"])

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Final screenshot and html dump:", x)
