import sys
import time
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.downloadmanager import DownloadManager
from OWDTestToolkit import DOM

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
        self.Settings = Settings(self)
        self.Browser  = Browser(self)
        self.DownloadManager = DownloadManager(self)
        self.testURL    = self.UTILS.general.get_os_variable("GLOBAL_DOWNLOAD_URL")
        self.fileName   = "ocupamucho.tgz"

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
        # Go to settings
        #
        self.Settings.launch()

        #
        # Go to downloads
        #
        self.Settings.downloads()

        #
        # Check the file is there
        #
        elem = (DOM.DownloadManager.download_element[0],
                DOM.DownloadManager.download_element[1] % (self.testURL + self.fileName))

        x = self.UTILS.element.getElement(elem,
            "Getting downloaded file [%s]" % self.fileName)

        self.UTILS.test.TEST(x is not None,
            "Checking we've got the file from the download list")

        text = self.marionette.execute_script("""
            return arguments[0].querySelector(".info").innerHTML;
        """, script_args=[x])

        if text:
            import re

            self.UTILS.reporting.logResult("info", "Info: " + text)

            pattern = r"^(\d)+(.(\d)+)*\s(MB|KB|B)\sof\s(\d)+(.(\d)+)*\sGB$"
            match = re.search(pattern, text)
            self.UTILS.test.TEST(match is not None, "Verify the text is : 'X' MB of 'Y' GB")

        #
        # Restart download list to start with an empty downloads list
        #
        self.DownloadManager.restartDownloadsList()