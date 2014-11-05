# 33934: Verify the donwloads list with a file name very long
#
# ** Prerrequisites
#       Having a downloads list with a download with very long name
# ** Procedure
#       1. Open settings app
#       2. Open Downloads
# ** Expected Results
#       A download with very long name is displayed successfully.
#       The file name is displayed in a line ended in "..."
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
        self.file_name = "prueba_archivo_con_nombre_muy_largo_de_30MB.rar"
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

        #
        # Check the file is there
        #
        entry_name = self.download_manager.get_download_entry(self.data_url).find_element(*('css selector', 'p.fileName'))
        value = self.UTILS.element.get_css_value(entry_name, "text-overflow")
        is_ellipsis = self.UTILS.element.is_ellipsis_active(entry_name)

        self.UTILS.test.test(value == "ellipsis" and is_ellipsis,
                             "Download list shows ellipsis(...) for a long entry [{}]".format(self.file_name))
