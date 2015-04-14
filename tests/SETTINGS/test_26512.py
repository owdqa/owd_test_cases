#===============================================================================
# 26512: Wi-Fi- verify its status and that can be activated from this menu
#
# Procedure:
# 1- Open Settings app
# 2- Go to Networking & Connectivity
# 3- Verify how the Wi-Fi is and try to activate it
#
# Expected results:
# The Wi-Fi is disabled. It can be activated from this menu
#===============================================================================

from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(FireCTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

        self.wifi_name = self.UTILS.general.get_config_variable("ssid", "wifi")
        self.wifi_pass = self.UTILS.general.get_config_variable("password", "wifi")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.settings.launch()
        self.settings.wifi()
        self.settings.connect_to_wifi(self.wifi_name, self.wifi_pass)

        self.UTILS.test.test(self.UTILS.network.is_network_type_enabled("wifi") == True, "Wifi mode is now enabled.")
