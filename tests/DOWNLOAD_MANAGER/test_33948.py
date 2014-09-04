# 33948: Verify that a file with size >=1 MB and <1GB is displayed as MB
# ** Procedure
#       1. Open a web pag in the browser which we can download files
#       2. Click on a file with size >=1 MB and <1GB to download it
#       3. Opening Settings / Download list during the download process
# ** Expected Results
#       The user can see the total file size and the downloaded file size during 
#       the download process. The sizes ares displayed as MB
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
        self.test_url = self.UTILS.general.get_os_variable("GLOBAL_DOWNLOAD_URL")
        self.file_name = "105MB.rar"
        self.data_url = "{}/{}".format(self.test_url, self.file_name)

        # make the download process slower
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
        time.sleep(5)

        self.apps.kill_all()
        time.sleep(2)

        self.settings.launch()
        self.settings.downloads()

        # Verify status downloading using data-state="downloading".
        self.download_manager.verify_download_status(self.data_url, "downloading")
        download_info = self.download_manager.get_download_info(self.data_url)

        match = re.search(r"(\d)+(.(\d)+)*\s(GB|MB|KB)\sof\s(\d)+(.(\d)+)*\sMB$", download_info.text)
        self.UTILS.test.TEST(match is not None, "Verify the the text is: 'X' MB of 'Y' MB")