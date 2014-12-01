#===============================================================================
# 33949: Verify that a file with size >1GB is displayed as GB
#
# Pre-requisites:
# Having a URL with several downloads to test download manager https://owd.tid.es/dm/
#
# Procedure:
# 1. Open a web pag in the browser which we can download files
# 2. Click on a file with size >1GB to download it
# 3. Opening Settings / Download list during the download process
#
# Expected results:
# The user can see the total file size and the downloaded file size during the
# download process. The sizes ares displayed as GB
#===============================================================================

import time
import re
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
        self.test_url = self.UTILS.general.get_config_variable("GLOBAL_DOWNLOAD_URL")
        self.file_name = "1GB.rar"
        self.data_url = "{}/{}".format(self.test_url, self.file_name)

        # make the download process slower
        self.data_layer.connect_to_cell_data()
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
        self.UTILS.statusbar.wait_for_notification_toaster_title(text="Download started", notif_text="Downloading",
                                                                 timeout=15)
        time.sleep(5)

        self.apps.kill_all()
        time.sleep(2)

        self.settings.launch()
        self.settings.downloads()

        # Verify status downloading using data-state="downloading".
        self.download_manager.verify_download_status(self.data_url, "downloading")
        download_info = self.download_manager.get_download_info(self.data_url)

        match = re.search(r"(\d)+(.(\d)+)*\s(GB|MB|KB)\sof\s(\d)+(.(\d)+)*\sGB$", download_info.text)
        self.UTILS.test.test(match is not None, "Verify the the text is: 'X' GB of 'Y' GB")

        time.sleep(3)
        self.download_manager.stop_download(self.data_url, True)
