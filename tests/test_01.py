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
from OWDTestToolkit.apps import Contacts
from OWDTestToolkit.utils import UTILS
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):
    def setUp(self):
        
        #
        # Set up child objects...
        #
        # Standard.
        GaiaTestCase.setUp(self)
        self.UTILS     = UTILS(self)

        # Specific for this test.
        self.contacts = Contacts(self)

        self.test_num = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM") 
        self.test_contacts = [MockContact(tel = {'type': 'Mobile', 'value': self.test_num},
            givenName = "M" + str(i + 1)) for i in range(5)]

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Brief test description
        #
        self.contacts.launch()

        self.contacts.createNewContact(self.test_contacts[0])
        self.contacts.mergeCreateNewContact(self.test_contacts[1])