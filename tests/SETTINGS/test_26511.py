#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
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
        x.tap()

        self.UTILS.network.waitForNetworkItemEnabled("airplane")

        self.UTILS.test.TEST(self.UTILS.network.isNetworkTypeEnabled("airplane") == True,
                             "Airplane mode is now enabled.")
        self.UTILS.test.TEST(self.data_layer.get_setting('ril.radio.disabled') == True,
                             "Radio functionality is now disabled.")
