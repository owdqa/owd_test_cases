#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

        self.wifi_name = self.UTILS.general.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user = self.UTILS.general.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass = self.UTILS.general.get_os_variable("GLOBAL_WIFI_PASSWORD")

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        self.settings.launch()

        # self.settings.wifi()
   
        # self.settings.wifi_switchOn()
   
        #
        # wifi_connect method already calls wifi() and wifi_switchOn()
        #
        self.settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)
   
        self.UTILS.test.TEST(self.UTILS.network.isNetworkTypeEnabled("wifi") == True, "Wifi mode is now enabled.")
