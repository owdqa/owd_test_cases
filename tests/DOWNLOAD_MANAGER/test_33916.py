# 33916: Press "Delete" in unable to open file screen
# ** Procedure
#       1. Download a not supported file ".rar, .doc..."
#       2. Open download list
#       3. Tap on the file
#       ER1
#       4. Press delete button and verify that
#       ER2
#       4. Press Delete button in confirmation screen
#       ER3
# ** Expected Results
#       ER1 A screen "unable to open file" is displayed with the buttons "Keep file" and "Delete"
#       ER2 A confirmation screen is displayed
#       ER3 The file is deleted and the user returns to donwload list
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
        self.file_name = "11MB.rar"
        self.data_url = "{}/{}".format(self.test_url, self.file_name)

        self.connect_to_network()
        self.settings.launch()
        self.settings.downloads()
        self.download_manager.clean_downloads_list()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        self.browser.launch()
        self.browser.open_url(self.test_url)

        self.download_manager.download_file(self.file_name)
        self.UTILS.statusbar.wait_for_notification_toaster_title("Download complete", timeout=60)
        time.sleep(5)

        self.apps.kill_all()
        time.sleep(2)
        previous_number_of_pictures = len(self.data_layer.sdcard_files())

        self.settings.launch()
        self.settings.downloads()
        self.download_manager.open_download(self.data_url)
        self.download_manager.open_download_delete_file()

        elem = (DOM.DownloadManager.download_element[0],
                DOM.DownloadManager.download_element[1].format(self.data_url))
        self.UTILS.element.waitForNotElements(elem, "Download is not there")

        # Check that picture saved to SD card
        self.wait_for_condition(
            lambda m: len(self.data_layer.sdcard_files()) == previous_number_of_pictures - 1, 20)
        self.assertEqual(len(self.data_layer.sdcard_files()), previous_number_of_pictures - 1)
