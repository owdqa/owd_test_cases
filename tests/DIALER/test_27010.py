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
        self.cont2 = MockContacts().Contact_2
        self.cont3 = MockContacts().Contact_3
        self.cont1["tel"]["value"]  = "+34111111111"
        self.data_layer.insert_contact(self.cont1)
        self.data_layer.insert_contact(self.cont2)
        self.data_layer.insert_contact(self.cont3)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.dialer.launch()
        self.dialer.enterNumber("1111")
        
        x = self.UTILS.getElement(DOM.Dialer.suggestion_item, "Suggestion item")
        self.UTILS.TEST(self.cont1["tel"]["value"] in x.text, 
                        "'%s' is shown as a suggestion (it was '%s')." %\
                        (self.cont1["tel"]["value"], x.text))

