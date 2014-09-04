# 33912: Verify that a user can delete a download in progress
# ** Procedure
#       1. Opening Settings app
#       2. Opening Donwloads list
#       3. Press Edit button
#       4. Select  a download in progress
#       5. Press Delete button
#       6. Press Delete button in confirmation screen
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

        self.browser = Browser(self)
        self.settings = Settings(self)
        self.download_manager = DownloadManager(self)
        self.test_url = self.UTILS.general.get_os_variable("GLOBAL_DOWNLOAD_URL")
        self.file_name = "22MB.rar"
        self.data_url = "{}/{}".format(self.test_url, self.file_name)

        self.data_layer.connect_to_cell_data()
        self.settings.launch()
        self.settings.downloads()
        self.download_manager.clean_downloads_list()

        # TODO - Remove this block when bug 1050225 is RESOLVED
        # We're doing this so that we have a previously completed download
        # and we can see the in progress download entry in the downloads list
        self.dummy_file = "Toast.doc"
        self.browser.launch()
        self.browser.open_url(self.test_url)
        self.download_manager.download_file(self.dummy_file)
        self.UTILS.statusbar.wait_for_notification_toaster_title("Download complete", timeout=60)
        time.sleep(5)
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        self.browser.launch()
        self.browser.open_url(self.test_url)

        self.download_manager.download_file(self.file_name)
        self.UTILS.statusbar.wait_for_notification_toaster_title("Download started", "Downloading", timeout=15)

        self.apps.kill_all()
        time.sleep(2)

        self.settings.launch()
        self.settings.downloads()

        # Verify status downloading using data-state="downloading".
        self.download_manager.verify_download_status(self.data_url, "downloading")
        self.download_manager.verify_download_graphical_status(self.data_url, "downloading")

        self.UTILS.statusbar.wait_for_notification_toaster_title("Download complete", frame_to_change=DOM.Settings.frame_locator, timeout=240)
        previous_number_of_pictures = len(self.data_layer.sdcard_files())
        self.UTILS.reporting.logResult('info', "Previous: {}".format(previous_number_of_pictures))
        
        # Delete download
        self.download_manager.delete_download(self.data_url)

        self.UTILS.reporting.logResult('info', "Current: {}".format(len(self.data_layer.sdcard_files())))
        # Check that picture saved to SD card
        self.wait_for_condition(
            lambda m: len(self.data_layer.sdcard_files()) == previous_number_of_pictures - 1, 20)
        self.assertEqual(len(self.data_layer.sdcard_files()), previous_number_of_pictures - 1)
