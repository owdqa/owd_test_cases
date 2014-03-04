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
from OWDTestToolkit.apps import Dialer
from tests._mock_data.contacts import MockContact

class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        
        self.cont1 = MockContact(tel=[{"type": "Mobile", "value": "111111111"}])
        self.UTILS.insertContact(self.cont1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.dialer.launch()
        self.dialer.enterNumber("1111")
        
        x = self.UTILS.getElement(DOM.Dialer.suggestion_item, "Suggestion item")
        self.UTILS.TEST(self.cont1["tel"][0]["value"] in x.text, 
                        "'{}' is shown as a suggestion (it was '{}').".format(self.cont1["tel"][0]["value"], x.text))

        self.dialer.enterNumber("2")
        self.UTILS.waitForNotElements(DOM.Dialer.suggestion_count, "Suggestion count")
