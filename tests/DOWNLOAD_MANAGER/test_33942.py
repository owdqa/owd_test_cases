# 33942: Verify that downloading icon is displayed in the status bar during the download process
# ** Procedure
#       1. Open a web pag in the browser which we can download files
#       2. Click on a file to download it
#
# ** Expected Results
#       Downloading icon is displayed in the status bar during the download process

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
        self.file_name = "11MB.rar"
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
        self.UTILS.statusbar.wait_for_notification_toaster_title(
            text="Download started", notif_text="Downloading", timeout=15)

        is_there = self.UTILS.statusbar.isIconInStatusBar(DOM.Statusbar.downloads)
        self.UTILS.test.test(is_there, "Verify that the download icon in status bar is active")
