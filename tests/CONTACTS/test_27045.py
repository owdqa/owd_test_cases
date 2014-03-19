#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
import time
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.gmail_user = self.UTILS.general.get_os_variable("GMAIL_1_USER")
        self.gmail_passwd = self.UTILS.general.get_os_variable("GMAIL_1_PASS")

        #
        # Create test contacts.
        #
        self.contact_list = [MockContact() for i in range(2)]
        self.contact_list[1]['email'] = {}

        map(self.UTILS.general.insertContact, self.contact_list)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.UTILS.network.getNetworkConnection()

        self.contacts.launch()

        self.contacts.import_gmail_login(self.gmail_user, self.gmail_passwd)

        x = self.UTILS.element.getElements(DOM.Contacts.import_conts_list, "Contact list", False)

        gmail_contacts = []
        for y in x:
            contact_name = y.get_attribute("data-search")
            if '#search#' not in contact_name:
                self.UTILS.reporting.logResult("info", "Adding '{}' to the list of available contacts.".\
                                    format(contact_name))
                gmail_contacts.append(contact_name)

        self.contacts.import_all()

        self.apps.kill_all()

        self.contacts.launch()

        self.UTILS.reporting.logResult("info", "Viewing contact '{}' ...".format(gmail_contacts[0]))
        self.contacts.view_contact("roytesterton.1@hotmail.com", False)

        editBTN = self.UTILS.element.getElement(DOM.Contacts.edit_details_button, "Edit details button")
        editBTN.tap()
        self.UTILS.element.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contacts' screen header")

        #
        # Enter the new contact details.
        #
        contact_fields = self.contacts.get_contact_fields()
        self.contacts.replace_str(contact_fields['givenName'], self.contact_list[1]["givenName"])
        self.contacts.replace_str(contact_fields['familyName'], self.contact_list[1]["familyName"])
        self.contacts.replace_str(contact_fields['tel'], self.contact_list[1]["tel"]["value"])
        self.contacts.replace_str(contact_fields['street'], self.contact_list[1]["adr"]["streetAddress"])
        self.contacts.replace_str(contact_fields['zip'], self.contact_list[1]["adr"]["postalCode"])
        self.contacts.replace_str(contact_fields['city'], self.contact_list[1]["adr"]["locality"])
        self.contacts.replace_str(contact_fields['country'], self.contact_list[1]["adr"]["countryName"])

        #
        # Save the changes
        #
        updateBTN = self.UTILS.element.getElement(DOM.Contacts.edit_update_button, "Edit 'update' button")
        updateBTN.tap()

        time.sleep(2)

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", x)
