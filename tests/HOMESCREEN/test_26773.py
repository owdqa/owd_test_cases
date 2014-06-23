#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM
from marionette import Actions
import time


class test_main(GaiaTestCase):

    _appName = "Juegos Gratis"
    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.actions    = Actions(self.marionette)
        self.settings   = Settings(self)
        self.EME        = EverythingMe(self)

        #
        # Ensure we have a connection
        #
        self.connect_to_network()
        self.UTILS.app.setPermission('Homescreen', 'geolocation', 'deny')

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Make sure our app isn't installed already.
        #
        self.UTILS.app.uninstallApp(self._appName)
    
        #
        # Install it.
        #
        self.EME.launch()
        x = self.EME.search_for_app(self._appName)
        actions = Actions(self.marionette)
        actions.press(x).wait(2).release()
        try:
            actions.perform()
        except:
            pass

        self.marionette.switch_to_frame()
        x = self.UTILS.element.getElement(DOM.GLOBAL.modal_alert_ok3, "OK button")
        x.tap()

        time.sleep(2)

        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)

        self.UTILS.app.uninstallApp(self._appName)