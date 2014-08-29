# 32238: Verify that an video file has several option to share it
# ** Procedure
#       1. Opening browser app
#       2. Download an video file
#       3. Opening Settings app
#       4. Opening Download list
#       5. Tap on the video downloaded
#       6. Select share option
# ** Expected Results
#       A list with some options to share the file is displayed
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.downloadmanager import DownloadManager
from OWDTestToolkit import DOM


class test_main(GaiaTestCase):

    button_locator = ('css selector', "button.icon")

    def setUp(self):

        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)

        self.browser = Browser(self)
        self.settings = Settings(self)
        self.download_manager = DownloadManager(self)

        self.test_url = self.UTILS.general.get_os_variable("GLOBAL_DOWNLOAD_URL")
        self.file_name = "clipcanvas_14348_H264_320x180.mp4"
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
        time.sleep(3)

        self.settings.launch()
        self.settings.downloads()
        self.download_manager.open_download(self.data_url)

        share_option = self.UTILS.element.getElement(DOM.DownloadManager.download_file_option_share,
                                                     "Getting Share option button")
        share_option.tap()

        self.marionette.switch_to_frame()
        share_menu = self.UTILS.element.getElement(DOM.GLOBAL.action_menu, "Share menu")
        options = share_menu.find_elements(*self.button_locator)
        self.UTILS.test.TEST(len(options) > 0, "A list with several options to share is shown")

        self._show_option(options)

    def _show_option(self, options):
        for option in options:
            self.UTILS.reporting.logResult('info', "Share option: {}".format(option.text))
