# 33913: Press "keep File" in unable to open file screen 
# ** Procedure
#       1. Download a not supported file ".rar, .doc..."
#       2. Open download list
#       3. Tap on the file and verify that a screen "unable to open file" is displayed 
#          with the buttons "Keep file" and "Delete"
#       4. Press "Keep File" button 
# ** Expected Results
#       The file is not deleted and the user returns to download list
import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.downloadmanager import DownloadManager
from OWDTestToolkit import DOM


class test_main(SpreadtrumTestCase):

    def setUp(self):

        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)

        self.browser = Browser(self)
        self.settings = Settings(self)
        self.download_manager = DownloadManager(self)
        self.test_url = self.UTILS.general.get_config_variable("download_url", "common")
        self.file_name = "11MB.rar"
        self.data_url = "{}/{}".format(self.test_url, self.file_name)

        self.connect_to_network()
        self.settings.launch()
        self.settings.downloads()
        self.download_manager.clean_downloads_list()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
 
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
        self.download_manager.open_download_keep_file()

        elem = (DOM.DownloadManager.download_element[0],
                DOM.DownloadManager.download_element[1].format(self.data_url))
        self.UTILS.element.waitForElements(elem, "Download is still there")
