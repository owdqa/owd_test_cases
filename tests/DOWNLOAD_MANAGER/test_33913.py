import sys
import time
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.downloadmanager import DownloadManager
from OWDTestToolkit import DOM


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
        self.browser = Browser(self)
        self.settings = Settings(self)
        self.downloadManager = DownloadManager(self)
        self.testURL    = self.UTILS.general.get_os_variable("GLOBAL_DOWNLOAD_URL")
        self.fileName   = "Toast.doc"

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Restart download list to start with an empty downloads list
        #
        self.downloadManager.clean_downloads_list()

        #
        # Tries several methods to get ANY network connection
        #
        self.UTILS.network.getNetworkConnection()


        #
        # Open the Browser application
        #
        self.browser.launch()

        #
        # Open our URL
        #
        self.browser.open_url(self.testURL)

        #
        # Download the file
        #
        self.downloadManager.downloadFile(self.fileName)

        #
        # Open the Settings application.
        #
        self.settings.launch()

        #
        # Tap Downloads List.
        #
        self.settings.downloads()
        time.sleep(5)

        #
        # Try to open the file - a position is required since weird things 
        # are happening with the file ID once downloaded
        #
        self.downloadManager.openDownload(self.testURL + self.fileName)

        #
        # Tap Open button.
        #
        self.UTILS.element.waitForElements(DOM.DownloadManager.download_file_option_open,
                                     "Waiting for Open file button")

        x = self.UTILS.element.getElement(DOM.DownloadManager.download_file_option_open,
            "Getting open button")
        x.tap()

        #
        # Wait for Delete button in Delete or Keep file screen
        #
        self.UTILS.element.waitForElements(DOM.DownloadManager.download_confirm,
            "Waiting for Delete file button", True, 10, True)

        x = self.UTILS.element.getElement(DOM.DownloadManager.download_confirm_yes,
                                    "Getting 'Delete' button")
        x.tap()


        #
        # Wait for Delete button in confirmation screen
        #
        self.UTILS.element.waitForElements(DOM.DownloadManager.download_confirm,
            "Waiting for confirm Keep file button", True, 10, True)

        x = self.UTILS.element.getElement(DOM.DownloadManager.download_confirm_no,
                                    "Getting cofirm 'Keep File' button")
        x.tap()


        #
        # To verify if the file continues in downloads list
        #
        self.downloadManager.openDownload(self.testURL + self.fileName)





