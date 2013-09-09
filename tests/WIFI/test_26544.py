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

class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.Settings   = Settings(self)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Open the Settings application.
        #
        self.Settings.launch()
        self.Settings.wifi()
        self.Settings.turn_wifi_on()
        
        x = self.UTILS.getElements(DOM.Settings.wifi_available_networks, "Available networks", False)
        
        self.UTILS.logResult("info", "Found %s networks" % len(x))
        
        _secured_num = 0
        for i in x:
            _secure1 = False
            _secure2 = False

            try:
                i.find_element("xpath", ".//aside[contains(@class,'secured')]")
                _secure1 = True
            except: pass

            try:
                i.find_element("xpath", ".//small[contains(text(), 'Secured')]")
                _secure2 = True
            except: pass
            
            try: _name    = i.find_element("xpath", ".//a").text
            except: _name = False
            
            if _name:
                self.UTILS.TEST(_secure1 == _secure2, 
                                "Network '%s' has matching 'network is secured' details (%s for icon and %s for description)." % \
                                (_name, _secure1, _secure2))
                
                
                
                
        