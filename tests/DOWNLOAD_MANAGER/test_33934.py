#
# Imports which are standard for all test cases.
#
import sys
import time
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.downloadmanager import DownloadManager
from OWDTestToolkit import DOM

#
# Imports particular to this test case.
#

class test_main(GaiaTestCase):

    #
    # Restart device to have a empty downloads list
    #
    #_RESTART_DEVICE = True

    def setUp(self):
        
        #
        # Set up child objects...
        #
        # Standard.
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)

        # Specific for this test.
        self.Browser = Browser(self)
        self.settings = Settings(self)
        self.DownloadManager = DownloadManager(self)
        self.testURL    = self.UTILS.general.get_os_variable("GLOBAL_DOWNLOAD_URL")
        self.fileName   = "prueba_archivo_con_nombre_muy_largo_de_30MB.rar"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Restart download list to start with an empty downloads list
        #
        self.DownloadManager.restartDownloadsList()

        #
        # Tries several methods to get ANY network connection
        #
        self.UTILS.network.getNetworkConnection()

        #
        # Open the Browser application
        #
        self.Browser.launch()

        #
        # Open our URL
        #
        self.Browser.open_url(self.testURL)
        time.sleep(5)

        #
        # Download the file
        #
        self.DownloadManager.downloadFile(self.fileName)

        #
        # Go to settings
        #
        self.settings.launch()

        #
        # Go to downloads
        #

        self.settings.downloads()

        #
        # Check the file is there
        #

        elem = (DOM.DownloadManager.download_element[0],
                DOM.DownloadManager.download_element[1] % (self.testURL + self.fileName))

        x = self.UTILS.element.getElement(elem,
            "Getting download file with a very long name")

        self.UTILS.test.TEST(x is not None,
            "Checking we've got the file from the donwload list")