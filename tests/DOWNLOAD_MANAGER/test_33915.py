# 33915: Try to open a .jpg file from download list

# ** Procedure
#       1. Open browser app
#       2. Open a webpage whitch  you can download files.
#       3. Download a .jpg file.
#       4. Open Settings/Downloads list
#       5. Tap on the file downloaded
# ** Expected Results
#       The file is opened successfully
#
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
        self.test_url = self.UTILS.general.get_config_variable("download_url", "common")
        self.file_name = "Crazy_Horse.jpg"
        self.data_url = "{}/{}".format(self.test_url, self.file_name)

        self.connect_to_network()
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
        self.UTILS.statusbar.wait_for_notification_toaster_title("Download complete", timeout=60)
        time.sleep(5)

        self.apps.kill_all()
        time.sleep(2)

        self.settings.launch()
        self.settings.downloads()
        self.download_manager.open_download(self.data_url)
        self.download_manager.tap_on_open_option()

        # Verify that the image is opened.
        self.UTILS.iframe.switchToFrame(*DOM.Gallery.frame_locator)
        title = self.UTILS.element.getElement(DOM.Gallery.file_name_header, "File name header")
        self.UTILS.test.test(title.text == self.file_name, "File name matches in Gallery")

        is_loaded = self.UTILS.element.waitForElements(DOM.Gallery.current_image_pic,
                                                       "Waiting for image to be loaded")
        self.UTILS.test.test(is_loaded, "Image has been loaded")
