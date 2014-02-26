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
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)
        
        self.Contact_1 = MockContact(tel = {'type': 'Mobile', 'value': '665666666'})
        self.num = self.Contact_1["tel"]["value"]

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Enter a number in the dialer.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        
        self.dialer.callThisNumber()
        
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
        x = self.UTILS.getElement(DOM.Dialer.hangup_bar_locator, "Hangup button")
        x.tap()
        
        self.marionette.switch_to_frame()
        x = DOM.Dialer.frame_locator_calling
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@%s,'%s')]" % (x[0],x[1])), "Calling iframe", True, 5)