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
        self.fileName   = "Crazy_Horse.jpg"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Restart download list to start with an empty downloads list
        #
        self.DownloadManager.clean_downloads_list()

        #
        # Restart notification bar
        #
        self.UTILS.statusbar.clearAllStatusBarNotifs()

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


        self.DownloadManager.clickDownloadNotifier("Download complete")
        # #
        # # Switch back to the messaging app.
        # #
        time.sleep(5)
        #self.UTILS.switchToFrame(*DOM.Gallery.frame_locator)
        self.UTILS.iframe.switchToFrame(*DOM.Gallery.frame_locator)

        
        isLoaded = self.UTILS.element.waitForElements(DOM.Gallery.current_image_pic2,
                                 "Waiting for image to be loaded")
        self.UTILS.test.TEST(isLoaded, "Checking image has been loaded")
