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
from OWDTestToolkit.apps import Dialer
from OWDTestToolkit.utils import UTILS
from tests._mock_data.contacts import MockContact

class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        
        self.test_num = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.test_contacts = [MockContact(tel = [{'type': 'Mobile', 'value': self.test_num}]) for i in range(2)]

     
        self.test_contacts[0]["givenName"] = "LongGivennamexxxxxxxxxxx"
        self.test_contacts[1]["familyName"] = "LongFamilynamexxxxxxxxxxx"

        for c in self.test_contacts:
            c["name"] = c["givenName"] + " " + c["familyName"]

        map(self.UTILS.insertContact, self.test_contacts)


    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.dialer.launch()
        self.dialer.callLog_clearAll()
        
        for contact in self.test_contacts:
            self.dialer.createMultipleCallLogEntries(contact["tel"]["value"], 1)
            
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of multiple entries:", x)
        
        x = self.UTILS.getElements(DOM.Dialer.call_log_numbers, "Call log entries", False)
        _scr = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "{} entries found.".format(len(x)), _scr)
        
        self.UTILS.logResult(False, "<b>NOTE: Cannot find a way to 'see' the dots!!</b>")

        i = 0
        for contact in self.test_contacts:
            _item = x[i].find_element("xpath", "//span[contains(text(), '{}')]".format(contact["givenName"][:6]))
            self.UTILS.logResult("info", "text {}: {}".format(i, _item.text))
            self.UTILS.logResult("info", "val  {}: {}".format(i, _item.get_attribute("value")))
            i += 1