#
# Imports which are standard for all test cases.
#
import sys
import re
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
        self.fileName    = "105MB.rar"

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
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



        #
        # Verify text during the download process (graphically)
        #
        elem = (DOM.DownloadManager.download_status_text_position[0],
                    DOM.DownloadManager.download_status_text_position[1].format(1))
        x = self.UTILS.element.getElement(elem,
                        "Obtain the text displayed to verify the text 'X' MB of 'Y' MB")

        match = re.search(r"(\d)+(.(\d)+)*\s(GB|MB|KB)\sof\s(\d)+(.(\d)+)*\s(GB|MB|KB)",
                             x.text)
        self.UTILS.test.TEST(match is not None, "Verify the the text is: 'X' MB of 'Y' MB")

        #
        # Verify status downloading using data-state="downloading".
        #
        elem = (DOM.DownloadManager.download_status_text_position[0],
                 DOM.DownloadManager.download_status_position[1].format(1))
        x =self.UTILS.element.getElement(elem, "Obtain the download state")
        self.UTILS.test.TEST("downloading" == x.get_attribute("data-state"),
                             "Verify that the status is downloading")

        #
        # Restarting Downloads list
        #
        self.downloadManager.restartDownloadsList()
