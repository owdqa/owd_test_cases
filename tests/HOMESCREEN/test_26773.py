#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *
from marionette import Actions


class test_main(GaiaTestCase):

    _appName = "Juegos Gratis"

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.actions    = Actions(self.marionette)
        self.settings   = Settings(self)
        self.EME        = EverythingMe(self)

        self.UTILS.setPermission('Homescreen', 'geolocation', 'deny')
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Make sure 'things' are as we expect them to be first.
        #
        self.UTILS.getNetworkConnection()
         
        #
        # Make sure our app isn't installed already.
        #
        self.UTILS.uninstallApp(self._appName)
                
        #
        # Install it.
        #
        self.EME.launch()
        x = self.EME.searchForApp(self._appName)
        self.actions.press(x).wait(2).release()
        self.actions.perform()
        
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.GLOBAL.modal_confirm_ok, "OK button")
        x.tap()
        
        time.sleep(2)
        self.UTILS.goHome()
        
        self.UTILS.uninstallApp(self._appName)
        
        
