# 32078: Press cancel button in audio file options screen
# ** Prerrequisites
#       Having an audio file downloaded which is displayed in download list
# ** Procedure
#       1. Open download list Settings/Downloads
#       2. Tap on an audio file
#       ER1
#       3. Press cancel button
#       ER2
# ** Expected Results
#       ER1 A menu with options "open, share and set as ringtone is displayed"
#       ER2 The user retunrs to download list
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
        self.file_name = "GOSPEL.mp3"
        self.data_url = "{}/{}".format(self.test_url, self.file_name)

        self.data_layer.connect_to_wifi()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        # Download and audio file
        self.settings.launch()
        self.settings.downloads()
        self.download_manager.clean_downloads_list()

        self.browser.launch()
        self.browser.open_url(self.test_url)

        self.download_manager.download_file(self.file_name)
        self.UTILS.statusbar.wait_for_notification_toaster_title("Download complete", timeout=60)
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.settings.launch()
        self.settings.downloads()
        self.download_manager.open_download(self.data_url)

        cancel_btn = self.UTILS.element.getElement(DOM.DownloadManager.download_file_option_cancel,
                                                   "Getting Open file button")
        cancel_btn.tap()
        self.UTILS.element.waitForElements(DOM.Settings.downloads_header,
                                           "Downloads header appears.", True, 20, True)
