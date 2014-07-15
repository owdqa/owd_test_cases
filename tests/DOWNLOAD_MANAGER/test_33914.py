#
# Imports which are standard for all test cases.
#
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
        self.Browser = Browser(self)
        self.Settings = Settings(self)
        self.DownloadManager = DownloadManager(self)
        self.testURL    = self.UTILS.general.get_os_variable("GLOBAL_DOWNLOAD_URL")
        self.fileName   = "GOSPEL.mp3"

    def tearDown(self):
        self.UTILS.reporting.reportResults()

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
        time.sleep(5)

        #
        # Try to open the file - a position is required since weird things 
        # are happening with the file ID once downloaded
        #
        self.DownloadManager.openDownload(self.testURL + self.fileName)


        self.UTILS.element.waitForElements(DOM.DownloadManager.download_file_option_open,
                                     "Getting Open file button")

        x = self.UTILS.element.getElement(DOM.DownloadManager.download_file_option_open,
            "Getting song title in music player")

        x.tap()



        self.UTILS.iframe.switchToFrame(*DOM.Music.frame_locator)
        time.sleep(10)

        #self.UTILS.element.waitForElements(DOM.Music.song_title,
        #                            "Getting song title")


        x = self.UTILS.element.getElement(DOM.Music.title_song,
            "Getting song title in music player")

        self.UTILS.test.TEST(x.text in self.fileName,
            "Verifying mp3 file is being played")