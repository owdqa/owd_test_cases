from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.browser = Browser(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        test_url = "http://qatecnico.blogspot.com.es/search/label/Automatizaci%C3%B3n%20de%20Pruebas"

        # Wifi needs to be off for this test to work.
        self.data_layer.connect_to_cell_data()

        # Open the browser app.
        self.browser.launch()

        self.browser.open_url(test_url)
