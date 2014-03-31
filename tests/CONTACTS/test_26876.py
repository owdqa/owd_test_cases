#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContact
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Get details of our test contacts.
        #
        self.contact = MockContact(tel=[{'type': 'Mobile', 'value': '555555555'},
                                        {'type': 'Mobile', 'value': '666666666'}])
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Search for our new contact.
        #
        self.contacts.view_contact(self.contact["name"])

        tel_counter = len(self.contact["tel"])
        for i in range(tel_counter):
            x = self.UTILS.element.getElement(("xpath", DOM.Contacts.view_contact_tels_xpath.\
                                       format(self.contact["tel"][i]["value"])),
                                       "Telephone number button for {}".format(self.contact["tel"][i]["value"]))
            self.UTILS.test.TEST(self.contact["tel"][i]["value"] in x.text,
                        "Phone number '{}' matches the expacted value ('{}')".\
                        format(x.text, self.contact["tel"][i]["value"]))

            self.UTILS.element.waitForElements(("id", DOM.Contacts.sms_button_specific_id.format(i)),
                                       "Send SMS button for {}".format(self.contact["tel"][i]["value"]))

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of contact:", x)
