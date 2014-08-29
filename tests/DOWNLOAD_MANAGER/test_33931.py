import sys
import time
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
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
        self.Settings = Settings(self)
        self.DownloadManager = DownloadManager(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Restart download list to start with an empty downloads list
        #
        self.DownloadManager.clean_downloads_list()


        #
        # Check "No downloads" label is there
        #

        x = self.UTILS.element.getElement(DOM.DownloadManager.download_empty_list_content,
                                "Getting empty list content")
        self.UTILS.test.TEST(x.text == "No downloads",
            "Verifying 'No downloads' message is displayed")



