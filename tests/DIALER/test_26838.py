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
        
        self.cont1 = MockContacts().Contact_1
        self.cont1["givenName"] = "Longgivennamexxxxxxxxxxx"
        self.cont1["name"] = self.cont1["givenName"] + " " + self.cont1["familyName"]
        self.data_layer.insert_contact(self.cont1)

        self.cont2 = MockContacts().Contact_2
        self.cont2["familyName"] = "Longfamilynamexxxxxxxxxxx"
        self.cont2["name"] = self.cont2["givenName"] + " " + self.cont2["familyName"]
        self.data_layer.insert_contact(self.cont2)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.dialer.launch()
        self.dialer.callLog_clearAll()
        
        self.dialer.createMultipleCallLogEntries(self.cont1["tel"]["value"], 1)
        self.dialer.createMultipleCallLogEntries(self.cont2["tel"]["value"], 1)
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of multiple entries:", x)
        
        x = self.UTILS.getElements(DOM.Dialer.call_log_numbers, "Call log entries", False)
        _scr = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "%s entries found." % len(x), _scr)
        
        self.UTILS.logResult(False, "<b>NOTE: Cannot find a way to 'see' the dots!!</b>")
        _item = x[0].find_element("xpath", "//span[contains(text(), '%s')]" % self.cont1["givenName"][:6])
        self.UTILS.logResult("info", "text 1: %s" % _item.text)
        self.UTILS.logResult("info", "val  1: %s" % _item.get_attribute("value"))
            
        _item = x[1].find_element("xpath", "//span[contains(text(), '%s')]" % self.cont2["givenName"][:6])
        self.UTILS.logResult("info", "text 2: %s" % _item.text)
            
            
            