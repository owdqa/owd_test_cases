#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *
from marionette import Actions


class test_main(GaiaTestCase):
    
    _appName = "Wikipedia"

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.actions    = Actions(self.marionette)
        self.settings   = Settings(self)
        self.eme        = EverythingMe(self)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Get a conection.
        #
        self.UTILS.getNetworkConnection()
        self.UTILS.uninstallApp(self._appName)
                
        #
        # Get the app.
        #
        self.eme.launch()
        x = self.eme.searchForApp(self._appName)
        
        self.UTILS.TEST(x, "Icon for " + self._appName + " is found.", True)
        
        #
        # Long-press the app to install it to the homescreen.
        #
        x = self.UTILS.getElement( ("xpath", DOM.EME.search_result_icon_xpath % self._appName),
                                   self._appName + " icon")
        
        self.actions.press(x).wait(2).release()
        self.actions.perform()
        
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.GLOBAL.modal_confirm_ok, "OK button")
        x.tap()
        
        time.sleep(2)
        self.UTILS.goHome()
        
        self.UTILS.uninstallApp(self._appName)
        
        
