# 33905: Verify that a user can delete a finished download file
# ** Prerrequisites
#       Having a finished download in downloads list
# ** Procedure
#       1. Open Settings app
#       2. Open Donwloads list
#       3. Press Edit button
#       4. Select a finished download
#       5. Press Delete button
#       6. Press Delete button in confirmation screen
#
# ** Expected Results
#       The download is deleted from downloads list and the file is removed from "SD CARD/Downloads"
#
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.downloadmanager import DownloadManager
from OWDTestToolkit import DOM


class test_main(GaiaTestCase):

    def setUp(self):

        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)

        # Specific for this test.
        self.browser = Browser(self)
        self.settings = Settings(self)
        self.download_manager = DownloadManager(self)
        self.test_url = self.UTILS.general.get_os_variable("GLOBAL_DOWNLOAD_URL")
        self.file_name = "Crazy_Horse.jpg"
        self.data_url = "{}/{}".format(self.test_url, self.file_name)

        self.connect_to_network()
        self.settings.launch()
        self.settings.downloads()
        self.download_manager.clean_downloads_list()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()
        
        self.browser.launch()
        self.browser.open_url(self.test_url)

        self.download_manager.download_file(self.file_name)
        self.UTILS.statusbar.wait_for_notification_toaster_title("Download complete", timeout=60)
        time.sleep(5)

        self.settings.launch()
        self.settings.downloads()

        time.sleep(3)

        self.download_manager.verify_download_status(self.data_url, "succeeded")
        self._enter_edit_mode()
        # self.download_manager.delete_download(self.data_url)
