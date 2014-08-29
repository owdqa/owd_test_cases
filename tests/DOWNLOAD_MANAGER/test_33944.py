import sys
import time
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.browser import Browser
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
        self.fileName    = "11MB.rar"
        
    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Verify that downloading icon disappears after completing the download
        #

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
        time.sleep(5)

        isThere = self.UTILS.statusbar.isIconInStatusBar(DOM.Statusbar.downloads)

        self.UTILS.test.TEST(isThere,
                 "Testing that the downloading icon is present in the statusbar")

        #
        # Wait for a "Completed" notification
        #
        x = self.DownloadManager.waitForDownloadNotifier("Download complete", self.fileName)

        self.UTILS.test.TEST(x,
            "Download of fileName [%s] completed and notified" % self.fileName)

        #
        # Check that the icon is now dismissed
        #
        isThere = self.UTILS.statusbar.isIconInStatusBar(DOM.Statusbar.downloads)

        self.UTILS.test.TEST(not isThere,
                 "Testing that the downloading icon is DISMISSED from the statusbar")