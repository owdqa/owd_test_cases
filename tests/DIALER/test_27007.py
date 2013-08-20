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
        
        self.cont1["tel"]["value"]  = "991234999"
        self.cont2["tel"]["value"]  = "999123499"
        self.cont3["tel"]["value"]  = "999912349"
        
        self.cont1["givenName"]  = "Aname"
        self.cont2["givenName"]  = "Bname"
        self.cont3["givenName"]  = "Cname"
        
        self.cont1["name"] = self.cont1["givenName"] + " " + self.cont1["familyName"]
        self.cont2["name"] = self.cont2["givenName"] + " " + self.cont2["familyName"]
        self.cont3["name"] = self.cont3["givenName"] + " " + self.cont3["familyName"]

        self.data_layer.insert_contact(self.cont1)
        self.data_layer.insert_contact(self.cont2)
        self.data_layer.insert_contact(self.cont3)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.dialer.launch()
        self.dialer.enterNumber("1234")
        
        x = self.UTILS.getElement(DOM.Dialer.suggestion_count, "Suggestion count")
        x.tap()
        x = self.UTILS.getElements(DOM.Dialer.suggestion_list, "Suggestion list")
        self.UTILS.TEST(len(x) == 3, "There are 3 contacts listed.")

        self.UTILS.TEST(self.cont1["name"] in x[0].text, 
                        "The first contact listed contains '%s' (it was '%s')." % \
                        (self.cont1["name"], x[0].text))

        self.UTILS.TEST(self.cont2["name"] in x[1].text, 
                        "The second contact listed contains '%s' (it was '%s')." % \
                        (self.cont2["name"], x[1].text))

        self.UTILS.TEST(self.cont3["name"] in x[2].text, 
                        "The third contact listed contains '%s' (it was '%s')." % \
                        (self.cont3["name"], x[2].text))
        
        self.UTILS.logResult("info", "Tapping 1st contact listed ...")
        x[0].tap()
        
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
        
        self.UTILS.waitForElements( ("xpath", DOM.Dialer.outgoing_call_numberXP % self.cont1["name"]),
                                    "Outgoing call found with number matching %s" % self.cont1["name"])
        
        time.sleep(2)
        self.dialer.hangUp()