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
        self.fileNames = [
           "105MB.rar",
           "41MB.rar",
           "30MB.rar"
        ]
        self.pre_progresses = []
        self.post_progresses = []

    def _getProgress(self, file, results):
        elem = (DOM.DownloadManager.download_element_progress[0],
                    DOM.DownloadManager.download_element_progress[1] % (self.testURL + file))

        x = self.UTILS.element.getElement(elem,
                "Getting downloaded file [%s]'s progress" % file)

        if x:
            value = x.get_attribute("value")
            self.UTILS.reporting.logComment("Value: " + value)
            results.append(int(value))


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

        #
        # Download the file
        #
        for elem in self.fileNames:
            self.DownloadManager.downloadFile(elem)
            time.sleep(5)

        #
        # Go to settings
        #
        self.settings.launch()

        #
        # Go to downloads
        #

        self.settings.downloads()

        #
        # Check the files are there
        #
        for downloadedFile in self.fileNames:
            elem = (DOM.DownloadManager.download_element[0],
                    DOM.DownloadManager.download_element[1] % (self.testURL + downloadedFile))

            x = self.UTILS.element.getElement(elem,
                "Getting downloaded file [%s]" % downloadedFile)

            self.UTILS.test.TEST(x is not None,
                "Checking we've got the file from the download list")

            #
            # Get the progresses
            #
            self._getProgress(downloadedFile, self.pre_progresses)

        #
        # Wait some time so that the download can continue for a while
        #
        time.sleep(15)

        for downloadedFile in self.fileNames:
            self._getProgress(downloadedFile, self.post_progresses)

        #
        # Compare progresses
        #
        i = 0;
        for elem in self.pre_progresses:
            self.UTILS.test.TEST(elem < self.post_progresses[i],
                "Verifying the progress of the downloads has continued")
            i += 1

