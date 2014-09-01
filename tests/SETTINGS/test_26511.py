#===============================================================================
# 26511: Airplane Mode- verify its functionality
#
# Procedure:
# 1- Open Settings app
# 2- Go to Network & Connectivity
# 3- Verify that Airplane Mode is disabled by default and the device has all
# its radio functionalities working well
# 4- Activate Airplane mode
# 5- Verify that all radio functionalities are disables until this mode is
# disabled again
#
# Expected results:
# Airplane Mode is disabled by default, when turning it on, all radio
# functionalities are disabled according to this mode
#===============================================================================
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.settings.launch()

        self.UTILS.test.TEST(self.UTILS.network.isNetworkTypeEnabled("airplane") == False,
                             "Airplane mode is disabled by default.")

        self.UTILS.reporting.logResult("info", "Turning airplane mode on ...")
        self.UTILS.test.TEST(True, "Getting airplane mode switch")
        x = self.UTILS.element.getElement(DOM.Settings.airplane_mode_switch, "Airplane mode switch")
        self.UTILS.test.TEST(True, "Airplane mode switch: {}".format(x))
        time.sleep(5)
        x.tap()

        self.UTILS.network.waitForNetworkItemEnabled("airplane")

        self.UTILS.test.TEST(self.UTILS.network.isNetworkTypeEnabled("airplane") == True,
                             "Airplane mode is now enabled.")
        self.UTILS.test.TEST(self.data_layer.get_setting('ril.radio.disabled') == True,
                             "Radio functionality is now disabled.")
