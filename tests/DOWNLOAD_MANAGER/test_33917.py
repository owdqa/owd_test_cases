# 33917: A user can open files by tappin on a download complete notification
# ** Procedure
#       1. Open browser app
#       2. Open a webpage whitch  you can download files.
#       3. Download a file which can be opened
#       4. Open the notification bar
#       5. Tap on the notification "Download complete"
# ** Expected Results
#      The file is opened successfully
#
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
        self.file_name = "Crazy_Horse.jpg"
        self.data_url = "{}/{}".format(self.test_url, self.file_name)

        self.data_layer.connect_to_wifi()
        self.settings.launch()
        self.settings.downloads()
        self.download_manager.clean_downloads_list()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.browser.launch()
        self.browser.open_url(self.test_url)
        self.download_manager.download_file(self.file_name)

        self.UTILS.statusbar.click_on_notification_title(
            "Download complete", frame_to_change=DOM.Gallery.frame_locator, timeout=60)

        # Verify that the image is opened.
        time.sleep(2)
        title = self.UTILS.element.getElement(DOM.Gallery.file_name_header, "File name header")
        self.UTILS.test.test(title.text == self.file_name, "File name matches in Gallery")
        self.UTILS.element.waitForElements(DOM.Gallery.download_manager_preview, "Waiting for image to be loaded")
