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
#
# Imports particular to this test case.
#

class test_main(GaiaTestCase):


    def setUp(self):
        
        #
        # Set up child objects...
        #
        # Standard.
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)

        # Specific for this test.
        self.Browser = Browser(self)
        self.Settings = Settings(self)
        self.DownloadManager = DownloadManager(self)
        self.testURL    = self.UTILS.general.get_os_variable("GLOBAL_DOWNLOAD_URL")
        self.fileName    = "105MB.rar"

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Restarting Downloads list
        #
        self.DownloadManager.clean_downloads_list()

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

        #
        # Download the file
        #
        self.DownloadManager.downloadFile(self.fileName)


        #
        # Open the Settings application.
        #
        self.Settings.launch()

        #
        # Tap Downloads List.
        #
        self.Settings.downloads()

        #
        # Stop the download
        #
        self.DownloadManager.stopDownloadByPosition(1, True)
        time.sleep(2)

        #
        # Restart the download
        #
        self.DownloadManager.restartDownloadByPosition(1, True)

        #
        # Restarting Downloads list
        #
        self.DownloadManager.clean_downloads_list()