# 33947: Verify that download continues, if you leave settings app during download process 
# ** Procedure
#       1. Open a web pag in the browser which we can download files
#       2. Click on a file to download it
#       3. Opening Settings / Download list during the download process
#       4. Press home button to leave the downloads list
#       5. Open the notification bar
#       ER1
#       6. Open Settings / Downloads list
#       ER2
# ** Expected Results
#       ER1.The user can see the download progress in the notification bar. After several minutes the download finishes and a notification is displayed
#       ER2. The file is displayed as completed

import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.downloadmanager import DownloadManager
from OWDTestToolkit import DOM


class test_main(FireCTestCase):

    def setUp(self):

        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)

        self.browser = Browser(self)
        self.settings = Settings(self)
        self.download_manager = DownloadManager(self)
        self.test_url = self.UTILS.general.get_config_variable("download_url", "common")
        self.file_name = "41MB.rar"
        self.data_url = "{}/{}".format(self.test_url, self.file_name)

        self.data_layer.connect_to_cell_data()
        self.settings.launch()
        self.settings.downloads()
        self.download_manager.clean_downloads_list()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        self.browser.launch()
        self.browser.open_url(self.test_url)

        self.download_manager.download_file(self.file_name)
        self.UTILS.statusbar.wait_for_notification_toaster_title(text="Download started", notif_text="Downloading", timeout=15)

        self.apps.kill_all()
        time.sleep(2)

        self.settings.launch()
        self.settings.downloads()

        # Verify status downloading using data-state="downloading".
        self.download_manager.verify_download_status(self.data_url, "downloading")
        self.download_manager.verify_download_graphical_status(self.data_url, "downloading")

        self.UTILS.home.touchHomeButton()

        self.UTILS.statusbar.displayStatusBar()
        self.UTILS.statusbar.wait_for_notification_statusbar_title("Downloading")
        self.UTILS.statusbar.hideStatusBar()

        self.UTILS.statusbar.wait_for_notification_toaster_title("Download complete", timeout=240)