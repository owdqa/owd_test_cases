#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContacts

class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)
        
        self.cont1 = MockContacts().Contact_1
        self.cont1["tel"]["value"]  = "111111111"
        self.data_layer.insert_contact(self.cont1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.dialer.launch()
        self.dialer.enterNumber("123")
        time.sleep(1)
        
        self.UTILS.waitForNotElements(DOM.Dialer.suggestion_count, "Suggestion count")
        self.UTILS.waitForNotElements(DOM.Dialer.suggestion_item, "Suggestion item")

        self.dialer.enterNumber("4")
        time.sleep(1)
        
        self.UTILS.waitForNotElements(DOM.Dialer.suggestion_count, "Suggestion count")
        self.UTILS.waitForNotElements(DOM.Dialer.suggestion_item, "Suggestion item")
