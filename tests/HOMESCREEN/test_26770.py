#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps import Settings
from OWDTestToolkit import DOM
import time



class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        
        self.UTILS      = UTILS(self)
        self.Settings   = Settings(self)
        self.EME        = EverythingMe(self)
        
        #
        # Don't prompt me for geolocation (this was broken recently in Gaia, so 'try' it).
        #
        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        except:
            self.UTILS.logComment("(Just FYI) Unable to automatically set Homescreen geolocation permission.")

        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
    
        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.UTILS.getNetworkConnection()
         
        #
        # Loop through a few groups to test.
        #
        self.EME.launch()
        x = self.UTILS.getElements(DOM.EME.groups, "Groups")
        if len(x) > 4:
            _max_groups = 4
        else:
            _max_groups = len(x)-1
            
        for i in range(0,_max_groups):
            x = self.UTILS.getElements(DOM.EME.groups, "Groups")
            _name = x[i].get_attribute("data-query")
            
            self.UTILS.logResult("info", "Checking group '%s' ..." % _name)
            self.EME.pick_group(_name)

            x = self.UTILS.screenShotOnErr()
            self.UTILS.logResult("info", "Screenshot of group icons: ", x)
                
            x = self.UTILS.getElement(DOM.EME.search_clear, "Clear search bar")
            x.tap()
            time.sleep(0.5)
         
