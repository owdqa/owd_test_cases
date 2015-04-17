# 33941: Verify that when a download completes, An event is displayed
# ** Procedure
#       1. Open a web page in the browser which we can download files
#       2. Click on a file to download it and wait the download time
# ** Expected Results
#       A event is displayed after completing the download

import time
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.video import Video
from OWDTestToolkit.apps.downloadmanager import DownloadManager
from OWDTestToolkit import DOM


class test_main(PixiTestCase):

    def setUp(self):

        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)

        self.browser = Browser(self)
        self.settings = Settings(self)
        self.download_manager = DownloadManager(self)
        self.video = Video(self)
        self.test_url = self.UTILS.general.get_config_variable("download_url", "common")
        self.file_name = "clipcanvas_14348_H264_320x180.mp4"
        self.data_url = "{}/{}".format(self.test_url, self.file_name)

        self.connect_to_network()
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
        self.UTILS.statusbar.wait_for_notification_toaster_title("Download complete", timeout=120)