# 33937: Verify that if the download is stopped, the  Status bar downloading icon is  dismissed
#
# ** Prerrequisites
#       Having a download in progress and a downloading icon in the status bar
# ** Procedure
#       1. Opening settings app
#       2. Opening Download list
#       3. Click on a download in progress
#       4. Click on "yes" button in confirmation screen

# ** Expected Results
#       Download is stopped and downloading icon is dismissed from the notification bar

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
        self.file_name = "105MB.rar"
        self.data_url = "{}/{}".format(self.test_url, self.file_name)

        # make the download process slower
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
        time.sleep(5)

        self.apps.kill_all()
        time.sleep(2)

        self.settings.launch()
        self.settings.downloads()

        # Verify status downloading using data-state="downloading".
        self.download_manager.verify_download_status(self.data_url, "downloading")
        self.download_manager.verify_download_graphical_status(self.data_url, "downloading")

        self.download_manager.stop_download(self.data_url, True)

        is_there = self.UTILS.statusbar.isIconInStatusBar(DOM.Statusbar.downloads)

        self.UTILS.test.test(not is_there, "Verify that the download icon in status bar is dismissed")
