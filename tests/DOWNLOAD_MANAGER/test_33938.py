# 33938: Verify that the download in progress notification is updated in the notification bar
#
# ** Prerrequisites
#       Having a download in prgoress and a downloading notification in notifications tray
# ** Procedure
#       1. Opening settings app
#       2. Opening Download list
#       ER1
#       3. Click on a download in progress
#       4. Click on "yes" button in confirmation screen
#       ER2
# ** Expected Results
#       ER1 A notification "Downloading" is displayed in the notification bar
#       ER2 The notificacion "Downloading" is updated and now displays "Download Stopped"
import time
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.downloadmanager import DownloadManager
from OWDTestToolkit import DOM


class test_main(PixiTestCase):

    def setUp(self):

        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)

        self.browser = Browser(self)
        self.settings = Settings(self)
        self.download_manager = DownloadManager(self)
        self.test_url = self.UTILS.general.get_config_variable("download_url", "common")
        self.file_name = "105MB.rar"
        self.data_url = "{}/{}".format(self.test_url, self.file_name)

        # make the download process slower
        self.data_layer.connect_to_cell_data()
        self.settings.launch()
        self.settings.downloads()
        self.download_manager.clean_downloads_list()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        self.browser.launch()
        self.browser.open_url(self.test_url)
        self.download_manager.download_file(self.file_name)
        self.UTILS.statusbar.wait_for_notification_toaster_title(text="Download started", notif_text="Downloading", timeout=15)
        time.sleep(5)

        self.apps.kill_all()
        time.sleep(2)

        self.settings.launch()
        self.settings.downloads()

        # Verify status downloading using data-state="downloading".
        self.download_manager.verify_download_status(self.data_url, "downloading")
        self.download_manager.verify_download_graphical_status(self.data_url, "downloading")

        self.download_manager.stop_download(self.data_url, True)
        self.UTILS.statusbar.wait_for_notification_statusbar_title("Download stopped")