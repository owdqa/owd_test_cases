# 33945: Verify that is possible download several files at the same time
# ** Procedure
#       1. Open a web pag in the browser which we can download files
#       2. Click on several files to download them
#       3. Opening Settings / Download list during the download process
# ** Expected Results
#       The user can see the progress bars during the downloads in the download
#       list. The progress bar grows during the download.

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
        self.file_names = [
            "105MB.rar",
            "41MB.rar",
            "30MB.rar"
        ]
        self.data_urls = ["{}/{}".format(self.test_url, file_name) for file_name in self.file_names]

        # Progress trackers
        self.pre_progresses = []
        self.post_progresses = []

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

    def _download_multiple_files(self, file):
        self.download_manager.download_file(file)
        self.UTILS.statusbar.wait_for_notification_toaster_title(
            "Download started", "Downloading", frame_to_change=DOM.Browser.frame_locator, timeout=15)
        self.browser.switch_to_content()
        time.sleep(5)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()
        self.browser.launch()
        self.browser.open_url(self.test_url)

        map(self._download_multiple_files, self.file_names)

        self.apps.kill_all()
        time.sleep(2)

        self.settings.launch()
        self.settings.downloads()

        for i in range(len(self.file_names)):
            # Check the download is there
            self.download_manager.get_download_entry(self.data_urls[i])
            # Check it is downloading
            self.download_manager.verify_download_status(self.data_urls[i], "downloading")
            self.download_manager.verify_download_graphical_status(self.data_urls[i], "downloading")
            # Append the progress
            self.pre_progresses.append(self.download_manager.get_download_progress(self.data_urls[i]))

        time.sleep(10)

        for i in range(len(self.file_names)):
            self.post_progresses.append(self.download_manager.get_download_progress(self.data_urls[i]))

        self.UTILS.reporting.logResult('info', "Initial progress array: {}".format(self.pre_progresses))
        self.UTILS.reporting.logResult('info', "Final progress array: {}".format(self.post_progresses))

        result = all([self.pre_progresses[i] < self.post_progresses[i]
                      for i in range(len(self.file_names))])
        self.UTILS.test.TEST(result, "The progress bar grows during the download.")
