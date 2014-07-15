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
from OWDTestToolkit.apps.video import Video
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
        self.UTILS = UTILS(self)

        # Specific for this test.
        self.browser = Browser(self)
        self.video = Video(self)
        self.settings = Settings(self)
        self.downloadManager = DownloadManager(self)
        self.testURL = self.UTILS.general.get_os_variable("GLOBAL_DOWNLOAD_URL")
        self.fileName = "clipcanvas_14348_H264_320x180.mp4"

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Restart download list to start with an empty downloads list
        #
        self.downloadManager.restartDownloadsList()

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
        # Opening video file
        #
        self.UTILS.element.waitForElements(DOM.DownloadManager.download_file_option_open,
                                     "Getting Open file button")

        x = self.UTILS.element.getElement(DOM.DownloadManager.download_file_option_open,
            "Getting Open file button")

        x.tap()


        #
        # Verifying video player
        #
        self.UTILS.iframe.switchToFrame(*DOM.Video.frame_locator)
        time.sleep(5)

        #
        # Taping in video player to display the video title
        #

        self.UTILS.element.waitForElements(DOM.Video.video_frame, "Getting video player")

        x = self.UTILS.element.getElement(DOM.Video.video_frame, "Getting video player")
        x.tap()

        #
        # Verifying video title
        #
        x = self.UTILS.element.getElement(DOM.Video.video_header,
                "Getting video  title in video player")

        self.UTILS.test.TEST(x.text in self.fileName,
            "Verifying video file is being played")
