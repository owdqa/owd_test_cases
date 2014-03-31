#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        self.num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        self.Contact_1 = MockContact()
        self.UTILS.general.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Create a call log.
        #
        self.dialer.launch()
        self.dialer.createMultipleCallLogEntries(self.num, 2)

        #
        # Add to our contact.
        #
        self.dialer.callLog_addToContact(self.num, self.Contact_1["name"], p_openCallLog=False)

        #
        # Verify that this contact has been modified in contacts.
        #
        self.contacts.launch()
        self.contacts.view_contact(self.Contact_1["name"])

        self.UTILS.element.waitForElements(("xpath", DOM.Contacts.view_contact_tels_xpath.format(self.num)),
                                    "Telephone number {} in contact".format(self.num))
