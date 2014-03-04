#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Dialer

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContact

class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        
        self.names = ["Aname", "Bname", "Cname"]
        self.values = ["991234999", "999123499", "999912349"]
        self.test_contacts = [MockContact(givenName=self.names[i],
            tel=[{"type":"mobile", "value": self.values[i]}]) for i in range(3)]

        #
        # This has to be done due to a MockContact malfunction. It does not
        # update the name field to the specified values of givenName and familyName
        #
        for c in self.test_contacts:
            c["name"] = c["givenName"] + " " + c["familyName"]

        map(self.UTILS.insertContact, self.test_contacts)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.dialer.launch()
    
        self.dialer.enterNumber("1234")
        
        x = self.UTILS.getElement(DOM.Dialer.suggestion_count, "Suggestion count")
        x.tap()
        x = self.UTILS.getElements(DOM.Dialer.suggestion_list, "Suggestion list")
        self.UTILS.TEST(len(x) == 3, "There are 3 contacts listed.")

        i = 0
        for c in self.test_contacts:
            self.UTILS.TEST(c["name"] in x[i].text,
                    "The first contact listed contains '{}' (it was '{}')".format(c["name"], x[i].text))
            i += 1

        x = self.UTILS.getElement(DOM.Dialer.suggestion_list_cancel, "Cancel button")
        x.tap()
        
        self.UTILS.waitForNotElements(DOM.Dialer.suggestion_list, "Suggestion list")
