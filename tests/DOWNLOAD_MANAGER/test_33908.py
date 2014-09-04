# 33908: Verify that a user can delete all download files from downloads list
# ** Procedure
#       1. OpenSettings app
#       2. Open Donwloads list
#       3. Press Edit button
#       ER1
#       4. Press select all button
#       ER2
#       5. Press Delete button
#       6. Press Delete button in confirmation screen
#       ER3
# ** Expected Results
#       ER1 Select all button is enabled and Deselect all button is disabled
#       ER2 Select all button is disabled and Deselect all button is enabled
#       ER3 All downloads are deleted and the files are removed from "SD CARD/Downloads"

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.downloadmanager import DownloadManager


class test_main(GaiaTestCase):

    #
    # Restart device to have a empty downloads list
    #
    #_RESTART_DEVICE = True

    def setUp(self):

        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)

        # Specific for this test.
        self.browser = Browser(self)
        self.settings = Settings(self)
        self.download_manager = DownloadManager(self)
        self.testURL = self.UTILS.general.get_os_variable("GLOBAL_DOWNLOAD_URL")
        self.file_names = ["Toast.doc", "Porridge.doc"]

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
        self.browser.open_url(self.testURL)

        map(self.download_manager.download_file, self.file_names)
        self.UTILS.statusbar.wait_for_notification_toaster_title("Download complete", timeout=60)
        time.sleep(5)

        previous_number_of_pictures = len(self.data_layer.sdcard_files())
        self.settings.launch()
        self.settings.downloads()

        # Delete All downloads
        self.download_manager.delete_all_downloads()

        # Check that picture saved to SD card
        self.wait_for_condition(
            lambda m: len(self.data_layer.sdcard_files()) == previous_number_of_pictures - len(self.file_names), 20)
        self.assertEqual(len(self.data_layer.sdcard_files()), previous_number_of_pictures - len(self.file_names))
