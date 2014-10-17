import time
from gaiatest import GaiaTestCase

class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.data_layer.enable_wifi()
        self.data_layer.connect_to_wifi()
        time.sleep(10)

    def tearDown(self):
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.disable_wifi()
        assert(not self.data_layer.is_wifi_enabled)
