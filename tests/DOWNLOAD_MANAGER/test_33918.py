# 33918: Try to open a .mp4 file from download list 
# ** Procedure
#       1. Open browser app
#       2. Open a webpage whitch  you can download files.
#       3. Download a .mp4 file. 
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
from OWDTestToolkit.apps.video import Video
from OWDTestToolkit.apps.downloadmanager import DownloadManager
from OWDTestToolkit import DOM


class test_main(GaiaTestCase):

    def setUp(self):

        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)

        self.browser = Browser(self)
        self.settings = Settings(self)
        self.download_manager = DownloadManager(self)
        self.video = Video(self)
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

        # Verifying video player
        self.UTILS.iframe.switchToFrame(*DOM.Video.frame_locator)
        result = self.video.is_this_video_being_played(self.file_name)
        self.UTILS.test.test(result, "This video [{}] is actually being played".format(self.file_name))