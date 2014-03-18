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
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact
import time


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.dialer     = Dialer(self)
    
        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContact(tel = {'type': 'Mobile', 'value': '665666666'})
        self.UTILS.insertContact(self.Contact_1)
        
        self._name = self.Contact_1["name"]
        self._num  = self.Contact_1["tel"]["value"]
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch dialer app.
        #
        self.dialer.launch()
        
        self.dialer.enterNumber(self._num)
        self.dialer.callThisNumber()

        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.UTILS.waitForElements( ("xpath", DOM.Dialer.outgoing_call_numberXP.format(self._name)),
                                    "Outgoing call found with name matching '{}'".format(self._name))

        time.sleep(2)

        self.dialer.hangUp()

